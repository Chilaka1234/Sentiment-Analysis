from django.shortcuts import render
import csv
from collections import Counter, defaultdict

def analyze_review(request):
    if request.method == "POST":
        review = request.POST.get("review")
        result = run_sentiment_analysis(review)
        sentiment = result
        return render(request, 'result.html', {'sentiment': sentiment, "rev": review, "ret": result})
    return render(request, 'review_form.html')

def load_reviews(filename):
    """Load and separate reviews into positive and negative lists."""
    pos_reviews, neg_reviews = [], []

    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for line in reader:
            if line["label"] == '1':
                pos_reviews.append(line["review"])
            else:
                neg_reviews.append(line["review"])

    return pos_reviews, neg_reviews

def build_vocabulary(pos_reviews, neg_reviews):
    """Create word frequency dictionaries and vocabulary set."""
    pos_words = [word for review in pos_reviews for word in review.split()]
    neg_words = [word for review in neg_reviews for word in review.split()]

    pos_word_counts = Counter(pos_words)
    neg_word_counts = Counter(neg_words)

    vocab = set(pos_word_counts.keys()).union(neg_word_counts.keys())
    return pos_word_counts, neg_word_counts, vocab, pos_words, neg_words

def calculate_probabilities(pos_word_counts, neg_word_counts, vocab, pos_words, neg_words, total_pos_reviews, total_neg_reviews):
    """Calculate word probabilities using Laplace smoothing."""
    word_probs = defaultdict(lambda: {
        "positive": 1 / (total_pos_reviews + 1),
        "negative": 1 / (total_neg_reviews + 1)
    })

    for word in vocab:
        word_probs[word]["positive"] = (pos_word_counts[word] + 1) / (len(pos_words) + len(vocab))
        word_probs[word]["negative"] = (neg_word_counts[word] + 1) / (len(neg_words) + len(vocab))

    return word_probs

def classify_review(review, word_probs, pos_prior, neg_prior, pos_words, neg_words, vocab):
    """Classify a given review using Naïve Bayes."""
    words_in_review = review.split()
    pos_prob, neg_prob = pos_prior, neg_prior

    for word in words_in_review:
        if word in word_probs:
            pos_prob *= word_probs[word]["positive"]
            neg_prob *= word_probs[word]["negative"]
        else:
            pos_prob *= 1 / (len(pos_words) + len(vocab))
            neg_prob *= 1 / (len(neg_words) + len(vocab))

    total_prob = pos_prob + neg_prob
    pos_prob /= total_prob
    neg_prob /= total_prob

    if 0.45 <= pos_prob <= 0.55 and 0.45 <= neg_prob <= 0.55:
        return "neutral"
    return "positive" if pos_prob > neg_prob else "negative"

def run_sentiment_analysis(review, filename='yelp_labelled.csv'):
    """Main function to process sentiment analysis."""
    pos_reviews, neg_reviews = load_reviews(filename)

    if not pos_reviews or not neg_reviews:
        return "neutral"

    pos_word_counts, neg_word_counts, vocab, pos_words, neg_words = build_vocabulary(pos_reviews, neg_reviews)

    total_pos_reviews = len(pos_reviews)
    total_neg_reviews = len(neg_reviews)
    total_reviews = total_pos_reviews + total_neg_reviews

    if total_reviews == 0:
        return "neutral"

    pos_prior = total_pos_reviews / total_reviews
    neg_prior = total_neg_reviews / total_reviews

    word_probs = calculate_probabilities(
        pos_word_counts,
        neg_word_counts,
        vocab,
        pos_words,
        neg_words,
        total_pos_reviews,
        total_neg_reviews,
    )

    return classify_review(review, word_probs, pos_prior, neg_prior, pos_words, neg_words, vocab)
