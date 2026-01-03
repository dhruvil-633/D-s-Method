class IntradayWriter:
    def __init__(self, db):
        self.db = db
        self.feature_buffer = []
        self.fusion_buffer = []

    def add_feature(self, row):
        self.feature_buffer.append(row)
        if len(self.feature_buffer) >= 100:
            self.flush_features()

    def add_fusion(self, row):
        self.fusion_buffer.append(row)
        if len(self.fusion_buffer) >= 100:
            self.flush_fusion()

    def flush_features(self):
        self.db.insert_many("intraday_features", self.feature_buffer)
        self.feature_buffer.clear()

    def flush_fusion(self):
        self.db.insert_many("fusion_outputs", self.fusion_buffer)
        self.fusion_buffer.clear()
