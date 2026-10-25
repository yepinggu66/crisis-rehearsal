# -*- coding: utf-8 -*-
"""
本地图谱适配器（ZEP_LOCAL=1 时接管 Zep Cloud）
================================================
目的：让 MiroFish 在没有任何云服务的情况下跑通「本体 → 建图 → 仿真 → 报告」全流程。

实现方式：用一个 duck-typed 的本地客户端替换 `zep_cloud.client.Zep`，
支持 MiroFish 实际用到的全部方法：
  graph.create/get/delete/set_ontology/add/search
  graph.node.get/get_edges/with_raw_response.get_by_graph_id
  graph.edge.with_raw_response.get_by_graph_id
  graph.episode.get/get_by_graph_id
  batch.create/add/process/get/list/list_items

实体/关系抽取用本地或云端 LLM（读 .env 的 LLM_* 配置）；
抽取失败时退化为规则抽取，保证流程不中断。
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
import uuid
from types import SimpleNamespace

from ..config import Config
from .logger import get_logger

logger = get_logger("mirofish.zep_local")

STORE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "local_zep")
STORE_DIR = os.path.abspath(STORE_DIR)


# ---------------------------------------------------------------- 存储
class _Store:
    def __init__(self):
        self.lock = threading.RLock()
        self.graphs: dict[str, dict] = {}
        os.makedirs(STORE_DIR, exist_ok=True)
        self._load()

    def _path(self, graph_id: str) -> str:
        return os.path.join(STORE_DIR, f"{graph_id}.json")

    def _load(self):
        for fn in os.listdir(STORE_DIR):
            if fn.endswith(".json"):
                try:
                    data = json.load(open(os.path.join(STORE_DIR, fn), encoding="utf-8"))
                    self.graphs[data["graph_id"]] = data
                except Exception:
                    pass

    def save(self, graph_id: str):
        with self.lock:
            json.dump(self.graphs[graph_id], open(self._path(graph_id), "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)


STORE = _Store()


# ---------------------------------------------------------------- LLM 抽取
def _llm_extract(text: str, ontology: dict) -> dict:
    """调用 LLM 从文本中抽取实体与关系；失败返回 {}。"""
    from openai import OpenAI

    base = (Config.LLM_BASE_URL or "").rstrip("/")
    key = Config.LLM_API_KEY or "local"
    model = Config.LLM_MODEL_NAME or "gpt-4o-mini"
    if not base:
        return {}

    ent_types = [e.get("name") for e in ontology.get("entity_types", [])][:12]
    edge_types = [e.get("name") for e in ontology.get("edge_types", [])][:12]
    prompt = (
        "你是知识图谱抽取器。请从下面的文本中抽取实体和关系，只输出 JSON，不要解释。\n"
        f"实体类型只能从这些里选：{ent_types}\n"
        f"关系类型只能从这些里选：{edge_types}\n"
        'JSON 结构：{"entities":[{"name":"", "type":"", "summary":"一句话", "attributes":{}}],'
        '"edges":[{"source":"实体名","target":"实体名","name":"关系类型","fact":"一句话事实"}]}\n'
        "最多 12 个实体、15 条关系。\n\n文本：\n" + text[:6000]
    )
    try:
        client = OpenAI(api_key=key, base_url=base, timeout=900, max_retries=0)
        kwargs = dict(model=model, messages=[{"role": "user", "content": prompt}],
                      temperature=0.2, max_tokens=1600)
        try:
            resp = client.chat.completions.create(
                extra_body={"chat_template_kwargs": {"enable_thinking": False}}, **kwargs)
        except Exception:
            resp = client.chat.completions.create(**kwargs)
        content = (resp.choices[0].message.content or "").strip()
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"```\s*$", "", content).strip()
        start = content.find("{")
        if start < 0:
            return {}
        try:
            data, _ = json.JSONDecoder().raw_decode(content[start:])
            return data if isinstance(data, dict) else {}
        except Exception:
            m = re.search(r"\{[\s\S]*\}", content)
            if not m:
                return {}
            try:
                return json.loads(m.group(0))
            except Exception:
                return {}
    except Exception as e:
        logger.warning("local zep extraction failed: %s", e)
        return {}


_ENTITY_PATTERNS = [
    r"「([^」]{2,14})」", r"“([^”]{2,14})”", r"'([^']{2,14})'",
    r"《([^》]{2,16})》",
    r"([\u4e00-\u9fa5A-Za-z0-9]{2,12}(?:公司|集团|网络|品牌|月饼|平台|网信办|监管局|市场监管|消费者协会))",
]


def _heuristic_extract(text: str, ontology: dict) -> dict:
    """规则抽取：从引号/机构后缀中提实体，按句共现连边。"""
    types = [e.get("name") for e in ontology.get("entity_types", [])] or ["Entity"]
    edge_types = [e.get("name") for e in ontology.get("edge_types", [])] or ["RELATED_TO"]
    names = []
    for pat in _ENTITY_PATTERNS:
        for m in re.findall(pat, text):
            m = m.strip()
            if 2 <= len(m) <= 20 and m not in names:
                names.append(m)
    sents = [x.strip() for x in re.split(r"[。！？\n]", text) if len(x.strip()) > 8][:10]

    # 没有抽到实体时，用句子片段兜底
    if not names:
        names = [x[:14] for x in sents[:6]]

    entities = []
    for i, nm in enumerate(names[:12]):
        related = next((x for x in sents if nm in x), "")
        entities.append({"name": nm, "type": types[i % len(types)],
                         "summary": (related or nm)[:120], "attributes": {}})

    edges = []
    for i, sent in enumerate(sents):
        hit = [e["name"] for e in entities if e["name"] in sent]
        for a, b in zip(hit, hit[1:]):
            edges.append({"source": a, "target": b,
                          "name": edge_types[len(edges) % len(edge_types)],
                          "fact": sent[:120]})
    return {"entities": entities, "edges": edges}


def _ingest(graph: dict, texts: list[str]):
    """对每段文本抽取实体/关系，合并进图。"""
    ontology = graph.get("ontology") or {}
    existing = {n["name"]: n for n in graph["nodes"]}
    fast = os.environ.get("ZEP_LOCAL_FAST", "").strip() in {"1", "true", "True", "yes"}
    for t in texts:
        data = _heuristic_extract(t, ontology) if fast else (_llm_extract(t, ontology) or _heuristic_extract(t, ontology))
        id_by_name = {}
        for e in data.get("entities", []):
            name = str(e.get("name") or "").strip()
            if not name:
                continue
            if name in existing:
                node = existing[name]
            else:
                node = {
                    "uuid_": str(uuid.uuid4()),
                    "name": name,
                    "labels": ["Entity", str(e.get("type") or "Entity")],
                    "summary": str(e.get("summary") or ""),
                    "attributes": e.get("attributes") or {},
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
                graph["nodes"].append(node)
                existing[name] = node
            id_by_name[name] = node["uuid_"]
        for ed in data.get("edges", []):
            s = str(ed.get("source") or "").strip()
            tgt = str(ed.get("target") or "").strip()
            if s in id_by_name and tgt in id_by_name and s != tgt:
                graph["edges"].append({
                    "uuid_": str(uuid.uuid4()),
                    "name": str(ed.get("name") or "RELATED_TO"),
                    "fact": str(ed.get("fact") or ""),
                    "source_node_uuid": id_by_name[s],
                    "target_node_uuid": id_by_name[tgt],
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                })
    STORE.save(graph["graph_id"])


# ---------------------------------------------------------------- 对象封装
def _node_obj(n: dict):
    return SimpleNamespace(uuid_=n["uuid_"], uuid=n["uuid_"], name=n["name"],
                           labels=n.get("labels") or ["Entity"],
                           summary=n.get("summary") or "",
                           attributes=n.get("attributes") or {},
                           created_at=n.get("created_at"))


def _edge_obj(e: dict):
    return SimpleNamespace(uuid_=e["uuid_"], uuid=e["uuid_"], name=e.get("name") or "",
                           fact=e.get("fact") or "",
                           source_node_uuid=e.get("source_node_uuid") or "",
                           target_node_uuid=e.get("target_node_uuid") or "",
                           attributes=e.get("attributes") or {},
                           labels=["EntityEdge"],
                           created_at=e.get("created_at"), valid_at=None,
                           invalid_at=None, expired_at=None)


def _score(text: str, q: str) -> int:
    if not text:
        return 0
    t = text.lower()
    ql = q.lower().strip()
    score = 0
    for ch in set(ql):
        if len(ch.strip()) and ch in t:
            score += 1
    for gram in {ql[i:i + 2] for i in range(max(len(ql) - 1, 1))}:
        if gram in t:
            score += 3
    return score


# ---------------------------------------------------------------- 客户端
class _Page:
    def __init__(self, data, headers=None):
        self.data = data
        self.headers = headers or {}


class _GraphNodeAPI:
    def __init__(self):
        self.with_raw_response = SimpleNamespace(get_by_graph_id=self._page)

    def _page(self, graph_id, limit=100, cursor=None):
        g = STORE.graphs.get(graph_id) or {"nodes": []}
        return _Page([_node_obj(n) for n in g["nodes"]])

    def get(self, uuid_=None, **kw):
        for g in STORE.graphs.values():
            for n in g["nodes"]:
                if n["uuid_"] == uuid_:
                    return _node_obj(n)
        raise KeyError(uuid_)

    def get_edges(self, node_uuid=None, **kw):
        out = []
        for g in STORE.graphs.values():
            for e in g["edges"]:
                if e.get("source_node_uuid") == node_uuid or e.get("target_node_uuid") == node_uuid:
                    out.append(_edge_obj(e))
        return out


class _GraphEdgeAPI:
    def __init__(self):
        self.with_raw_response = SimpleNamespace(get_by_graph_id=self._page)

    def _page(self, graph_id, limit=100, cursor=None):
        g = STORE.graphs.get(graph_id) or {"edges": []}
        return _Page([_edge_obj(e) for e in g["edges"]])

    def get(self, uuid_=None, **kw):
        for g in STORE.graphs.values():
            for e in g["edges"]:
                if e["uuid_"] == uuid_:
                    return _edge_obj(e)
        raise KeyError(uuid_)


class _GraphEpisodeAPI:
    def get(self, uuid_=None, **kw):
        for g in STORE.graphs.values():
            for ep in g.get("episodes", []):
                if ep["uuid_"] == uuid_:
                    return SimpleNamespace(uuid_=ep["uuid_"], content=ep["content"],
                                           processed=True, created_at=ep.get("created_at"))
        raise KeyError(uuid_)

    def get_by_graph_id(self, graph_id=None, lastn=50, **kw):
        g = STORE.graphs.get(graph_id) or {"episodes": []}
        eps = g.get("episodes", [])[-lastn:]
        return [SimpleNamespace(uuid_=e["uuid_"], content=e["content"], processed=True,
                                created_at=e.get("created_at")) for e in eps]


class _GraphAPI:
    def __init__(self):
        self.node = _GraphNodeAPI()
        self.edge = _GraphEdgeAPI()
        self.episode = _GraphEpisodeAPI()

    def create(self, graph_id=None, name=None, description=None, **kw):
        with STORE.lock:
            STORE.graphs[graph_id] = {"graph_id": graph_id, "name": name or graph_id,
                                      "description": description or "", "ontology": {},
                                      "nodes": [], "edges": [], "episodes": [],
                                      "batches": {}}
            STORE.save(graph_id)
        return SimpleNamespace(graph_id=graph_id, name=name)

    def get(self, graph_id=None, **kw):
        g = STORE.graphs.get(graph_id)
        if not g:
            raise KeyError(graph_id)
        return SimpleNamespace(graph_id=graph_id, name=g.get("name"),
                               description=g.get("description"))

    def delete(self, graph_id=None, **kw):
        STORE.graphs.pop(graph_id, None)
        try:
            os.remove(STORE._path(graph_id))
        except Exception:
            pass
        return {}

    def set_ontology(self, graph_ids=None, entities=None, edges=None, **kw):
        gid = (graph_ids or [None])[0]
        g = STORE.graphs.get(gid)
        if g is None:
            return {}
        def _names(obj):
            out = []
            for k in list(obj or {}):
                out.append({"name": k})
            return out
        g["ontology"] = {"entity_types": _names(entities), "edge_types": _names(edges)}
        STORE.save(gid)
        return {}

    def search(self, graph_id=None, query="", limit=10, scope="edges", reranker=None, **kw):
        g = STORE.graphs.get(graph_id) or {"nodes": [], "edges": []}
        nodes = sorted(g["nodes"], key=lambda n: _score(n.get("name", "") + " " + n.get("summary", ""), query),
                       reverse=True)[:limit]
        edges = sorted(g["edges"], key=lambda e: _score(e.get("fact", ""), query), reverse=True)[:limit]
        nodes = [n for n in nodes if _score(n.get("name", "") + " " + n.get("summary", ""), query) > 0] or nodes[:3]
        edges = [e for e in edges if _score(e.get("fact", ""), query) > 0] or edges[:3]
        return SimpleNamespace(nodes=[_node_obj(n) for n in nodes],
                               edges=[_edge_obj(e) for e in edges],
                               episodes=[])


class _BatchAPI:
    def create(self, metadata=None, **kw):
        bid = f"localbatch_{uuid.uuid4().hex[:12]}"
        _batch_meta[bid] = {"metadata": metadata or {}, "items": [], "status": "draft",
                            "processed": False}
        return SimpleNamespace(batch_id=bid, status="draft")

    def add(self, batch_id=None, items=None, **kw):
        b = _batch_meta.setdefault(batch_id, {"metadata": {}, "items": [], "status": "draft",
                                              "processed": False})
        out = []
        for it in items or []:
            idx = len(b["items"])
            ep_uuid = str(uuid.uuid4())
            b["items"].append({"sequence_index": idx, "episode_uuid": ep_uuid,
                               "source_uuid": ep_uuid, "status": "succeeded", "error": None,
                               "data": getattr(it, "data", ""), "type": getattr(it, "type", ""),
                               "graph_id": getattr(it, "graph_id", None)})
            out.append(SimpleNamespace(episode_uuid=ep_uuid, sequence_index=idx, status="succeeded"))
        return out

    def process(self, batch_id=None, **kw):
        b = _batch_meta.get(batch_id)
        if not b:
            raise KeyError(batch_id)
        if b.get("processed"):
            return {}
        # 收集 episode 文本，按 graph 分组抽取
        by_graph: dict[str, list[str]] = {}
        for it in b["items"]:
            gid = it.get("graph_id")
            if gid:
                by_graph.setdefault(gid, []).append(it.get("data") or "")
                g = STORE.graphs.get(gid)
                if g is not None:
                    g.setdefault("episodes", []).append(
                        {"uuid_": it["episode_uuid"], "content": it.get("data") or "",
                         "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")})
        for gid, texts in by_graph.items():
            g = STORE.graphs.get(gid)
            if g is not None:
                _ingest(g, texts)
        b["processed"] = True
        b["status"] = "succeeded"
        return {}

    def get(self, batch_id=None, **kw):
        b = _batch_meta.get(batch_id) or {"items": [], "status": "succeeded", "processed": True}
        n = len(b["items"])
        return SimpleNamespace(
            batch_id=batch_id, status=b.get("status") or ("succeeded" if b.get("processed") else "draft"),
            progress=SimpleNamespace(percent_complete=100.0 if b.get("processed") else 0.0,
                                     succeeded_items=n if b.get("processed") else 0,
                                     failed_items=0, pending_items=0 if b.get("processed") else n),
            items=[])

    def list(self, limit=100, cursor=None, **kw):
        batches = [SimpleNamespace(batch_id=k, status=v.get("status", "succeeded"),
                                   metadata=v.get("metadata") or {})
                   for k, v in _batch_meta.items()]
        return SimpleNamespace(batches=batches, next_cursor=None)

    def list_items(self, batch_id=None, limit=100, cursor=None, **kw):
        b = _batch_meta.get(batch_id) or {"items": []}
        items = [SimpleNamespace(sequence_index=i["sequence_index"], status=i["status"],
                                 episode_uuid=i["episode_uuid"], source_uuid=i["source_uuid"],
                                 error=None) for i in b["items"]]
        return SimpleNamespace(items=items, next_cursor=None)


_batch_meta: dict[str, dict] = {}


class LocalZep:
    """duck-typed 替代 zep_cloud.client.Zep。"""

    def __init__(self):
        self.graph = _GraphAPI()
        self.batch = _BatchAPI()


_CLIENT = None


def get_local_client() -> LocalZep:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = LocalZep()
        logger.info("LocalZep 已启用（本地图谱，无需 Zep Cloud）")
    return _CLIENT
