from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

MODEL_PATH = "spam_model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

MODEL = None
VECTORIZER = None


# ------------------------------------------------
# Load model if exists
# ------------------------------------------------
if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    MODEL = joblib.load(MODEL_PATH)
    VECTORIZER = joblib.load(VECTORIZER_PATH)


# ------------------------------------------------
# Training Data (250 samples)
# ------------------------------------------------
spam_samples = [
    "Buy cheap viagra now",
    "Win a lottery today",
    "Free money no strings attached",
    "Limited time offer",
    "Congratulations you won",
    "Earn money from home",
    "Act now claim your prize",
    "Exclusive deal just for you",
    "Click here to win",
    "Cheap meds online",
    "Get rich quick scheme",
    "Urgent response required",
    "Free gift card",
    "Cash bonus waiting",
    "Special promotion offer"
] * 9

ham_samples = [
    "Hello my friend",
    "Meeting scheduled for tomorrow",
    "Project update",
    "Invoice attached",
    "Happy birthday",
    "Let's have lunch",
    "Monthly report attached",
    "Please review the document",
    "Team meeting reminder",
    "Client feedback received",
    "Your order has shipped",
    "Family dinner tonight",
    "Office announcement",
    "Assignment submission",
    "Follow up on discussion"
] * 9

spam_samples = spam_samples[:125]
ham_samples = ham_samples[:125]

emails = spam_samples + ham_samples
labels = [1] * 125 + [0] * 125   # 1 = spam, 0 = ham


# ------------------------------------------------
# Train model if not already trained
# ------------------------------------------------
if MODEL is None or VECTORIZER is None:
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(emails)

    model = MultinomialNB()
    model.fit(X, labels)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    MODEL = model
    VECTORIZER = vectorizer

#   strategies - two strategies: rule-based and model-based
# ------------------------------------------------
# FINAL PREDICTION FUNCTION (BOOL)
# ------------------------------------------------
def predict_spam(text: str) -> bool:
    """
    True  -> SPAM
    False -> NOT SPAM
    """

    # -------- Rule-based strategy --------
    spam_keywords = [
        "free", "win", "winner", "lottery", "viagra",
        "cheap", "money", "prize", "bonus", "offer",
        "urgent", "click", "deal", "cash", "reward"
    ]

    text_lower = text.lower()
    rule_based = any(word in text_lower for word in spam_keywords)

    # -------- Model-based strategy --------
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        return rule_based

    X = VECTORIZER.transform([text])
    model_based = MODEL.predict(X)[0] == 1

    # -------- Final decision --------
    return rule_based or model_based

