import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

class EmergencyClassifier:
    def __init__(self):
        # Training data for basic classification
        self.data = [
            ("someone is following me and trying to attack", "Crime"),
            ("robbery in progress help", "Crime"),
            ("physical assault at the park", "Crime"),
            ("theft and harassment", "Crime"),
            ("harassment and stalking", "Crime"),
            
            ("person collapse chest pain", "Medical"),
            ("unconscious person bleeding", "Medical"),
            ("heavy breathing and fainting", "Medical"),
            ("allergic reaction and choking", "Medical"),
            ("severe injury and broken bone", "Medical"),
            
            ("huge fire in the building", "Fire"),
            ("smoke coming out of the kitchen", "Fire"),
            ("short circuit and sparks fire", "Fire"),
            ("bush fire spreading", "Fire"),
            ("gas leak and fire explosion", "Fire"),
            
            ("car accident at the intersection", "Accident"),
            ("bike crash and injury", "Accident"),
            ("truck collided with a pole", "Accident"),
            ("multiple vehicle pileup", "Accident"),
            ("hit and run accident", "Accident"),
            
            ("stuck in elevator help", "Other"),
            ("power outage and weird noise", "Other"),
            ("lost in the woods", "Other"),
            ("strange person loitering", "Other"),
            ("street lights not working", "Other")
        ]
        
        self.texts, self.labels = zip(*self.data)
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', MultinomialNB())
        ])
        self.model.fit(self.texts, self.labels)

    def classify(self, description):
        if not description or len(description.strip()) < 3:
            return "Other"
        try:
            return self.model.predict([description])[0]
        except Exception:
            return "Other"

# Global instance
classifier = EmergencyClassifier()
