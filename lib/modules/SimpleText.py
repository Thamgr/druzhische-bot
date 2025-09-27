class SimpleText:
    @staticmethod
    def render(config):
        # Handle both dict and direct text value
        if isinstance(config, dict):
            return config.get('text', '')
        return config