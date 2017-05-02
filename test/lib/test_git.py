from src.lib import git


def test_parse_describe_out():
    assert git.parse_describe_output('bf1a166') == {
        'commit': 'bf1a166',
        'dirty': False
    }
    assert git.parse_describe_output('bf1a166-dirty') == {
        'commit': 'bf1a166',
        'dirty': True
    }
    assert git.parse_describe_output('v1.80.1.0-SE1180022-9-gfd790f5') == {
        'commit': 'gfd790f5',
        'dirty': False,
        'revision': 9,
        'tag': 'v1.80.1.0-SE1180022'
    }
    assert git.parse_describe_output('v1.80.1.0-SE11800-9-gfd790f5-dirty') == {
        'commit': 'gfd790f5',
        'dirty': True,
        'revision': 9,
        'tag': 'v1.80.1.0-SE11800'
    }
    assert git.parse_describe_output('v1.80.1.0-SE1180022') == {
        'dirty': False,
        'tag': 'v1.80.1.0-SE1180022',
    }
    assert git.parse_describe_output('v1.80.1.0-SE1180022-dirty') == {
        'dirty': True,
        'tag': 'v1.80.1.0-SE1180022',
    }
