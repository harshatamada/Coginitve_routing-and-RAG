from persona_router import route_post_to_bots
from test_data import test_data

def evaluate():
    correct = 0
    total_predicted = 0
    total_actual = 0

    for item in test_data:
        preds, _, _ = route_post_to_bots(item["post"], threshold=0.4)
        pred_bots = [p["bot"] for p in preds]
        actual = item["expected"]

        correct_matches = set(pred_bots).intersection(set(actual))

        correct += len(correct_matches)
        total_predicted += len(pred_bots)
        total_actual += len(actual)

    precision = correct / total_predicted if total_predicted else 0
    recall = correct / total_actual if total_actual else 0

    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0

    print("Precision:", round(precision, 3))
    print("Recall:", round(recall, 3))
    print("F1 Score:", round(f1, 3))
    print("\nPost:", item["post"])
    print("Predicted:", pred_bots)
    print("Actual:", actual)

if __name__ == "__main__":
    evaluate()