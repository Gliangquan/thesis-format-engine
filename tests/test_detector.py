from thesis_format_engine.detector.engine import DetectionEngine
from thesis_format_engine.models.node import DocumentNode
from thesis_format_engine.models.rule import RegionRule, RuleSet


def test_detector_reports_missing_region_rule():
    engine = DetectionEngine()
    nodes = [DocumentNode(node_id="p-1", node_type="paragraph", region="Unknown")]
    rules = RuleSet(name="demo", regions=[RegionRule(region="Normal")])

    issues = engine.compare(nodes, rules)

    assert len(issues) == 1
    assert issues[0]["region"] == "Unknown"
