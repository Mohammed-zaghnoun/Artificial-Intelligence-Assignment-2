import math
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
SEED = 42
rng = np.random.default_rng(SEED)
def laplace(count, total, K, alpha=1.0):
    return (count + alpha) / (total + alpha * K) if total > 0 else 1.0 / K
def priors(df):
    vc = df["Rain"].value_counts()
    n = len(df)
    return {"Yes": vc.get("Yes",0)/n, "No": vc.get("No",0)/n}
def cond_prob(df, feature, value, rain_class):
    sub = df[df["Rain"] == rain_class]
    tot = len(sub)
    cnt = (sub[feature] == value).sum()
    p = (cnt / tot) if tot > 0 else 0.0
    return p, cnt, tot
class NaiveBayesCat:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
    def fit(self, X, y):
        self.classes = sorted(y.unique().tolist())
        self.cats = {c: sorted(X[c].unique().tolist()) for c in X.columns}
        self.prior = {cls: (y == cls).mean() for cls in self.classes}
        self.lk = {}
        for f in X.columns:
            self.lk[f] = {}
            K = len(self.cats[f])
            for cls in self.classes:
                Xc = X[y == cls]
                tot = len(Xc)
                self.lk[f][cls] = {}
                for v in self.cats[f]:
                    cnt = (Xc[f] == v).sum()
                    self.lk[f][cls][v] = laplace(cnt, tot, K, self.alpha)
        return self
    def proba_row(self, row):
        logp = {}
        for cls in self.classes:
            lp = math.log(self.prior[cls] + 1e-15)
            for f, v in row.items():
                K = len(self.cats[f])
                lk = self.lk[f][cls].get(v, 1.0 / K)
                lp += math.log(lk + 1e-15)
            logp[cls] = lp
        m = max(logp.values())
        exps = {c: math.exp(logp[c] - m) for c in self.classes}
        Z = sum(exps.values())
        return {c: exps[c]/Z for c in self.classes}
    def predict(self, X):
        return [max(self.proba_row(r).items(), key=lambda kv: kv[1])[0] for _, r in X.iterrows()]
def main():
    df = pd.read_csv("weather.csv")
    print("Loaded weather.csv:", df.shape, "\n")
    P = priors(df)
    print(f"P(Rain=Yes) = {P['Yes']:.4f}")
    print(f"P(Rain=No)  = {P['No']:.4f}")
    for feat, val in [("Humidity","High"), ("Cloudy","Yes")]:
        for cls in ["Yes","No"]:
            p, cnt, tot = cond_prob(df, feat, val, cls)
            print(f"P({feat}={val} | Rain={cls}) = {p:.4f}   [count={cnt}/{tot}]")
    for feat, K in [("Humidity",2), ("Cloudy",2)]:
        for val in (["High","Low"] if feat=="Humidity" else ["Yes","No"]):
            for cls in ["Yes","No"]:
                _, cnt, tot = cond_prob(df, feat, val, cls)
                ps = laplace(cnt, tot, K, alpha=1.0)
                print(f"P({feat}={val} | Rain={cls})_smoothed = {ps:.4f}   [count={cnt}/{tot}]")
    features = ["Humidity","Temperature","Wind","Cloudy"]
    target = "Rain"
    train_idx, test_idx = [], []
    for cls, grp in df.groupby(target):
        idx = grp.index.to_numpy()
        rng.shuffle(idx)
        n_test = max(1, int(len(idx)*0.2))
        test_idx += idx[:n_test].tolist()
        train_idx += idx[n_test:].tolist()
    train = df.loc[train_idx].reset_index(drop=True)
    test  = df.loc[test_idx].reset_index(drop=True)
    Xtr, ytr = train[features], train[target]
    Xte, yte = test[features], test[target]
    nb = NaiveBayesCat(alpha=1.0).fit(Xtr, ytr)

    # ---- USER INPUT FOR QUERY ----
    q_dict = {}
    for feature in ["Humidity","Temperature","Wind","Cloudy"]:
        val = input(f"Enter value for {feature}: ")
        q_dict[feature] = val
    q = pd.Series(q_dict)

    # ---- CALCULATE PROBABILITIES AND PREDICTION ----
    q_probs = nb.proba_row(q)
    # Ensure Yes/No prediction matches actual higher probability
    if q_probs["Yes"] > q_probs["No"]:
        q_pred = "Yes"
    else:
        q_pred = "No"

    # ---- Display clear Yes/No answer ----
    print("\n=== Prediction Result ===")
    print(f"It will rain? {q_pred} (Yes probability = {q_probs['Yes']:.4f}, No probability = {q_probs['No']:.4f})")
    print("========================\n")

    yhat = nb.predict(Xte)
    acc = (pd.Series(yhat).values == yte.values).mean()
    print("Train size:", len(train), " Test size:", len(test))
    print("Query:", dict(q))
    print("Query class probabilities:", {k: round(v,4) for k,v in q_probs.items()})
    print("Query predicted class:", q_pred)
    print(f"Test Accuracy: {acc:.4f}")
    model = {
        "alpha": 1.0,
        "classes": nb.classes,
        "priors": nb.prior,
        "feature_categories": nb.cats,
        "feature_likelihoods": nb.lk,
    }
    with open("naive_bayes_model.json","w",encoding="utf-8") as f:
        json.dump(model, f, indent=2)
    print("Save naive_bayes_model.json")

    _, cnt_h_y, tot_y = cond_prob(df, "Humidity", "High", "Yes")
    _, cnt_h_n, tot_n = cond_prob(df, "Humidity", "High", "No")
    p_h_y = laplace(cnt_h_y, tot_y, 2, alpha=1.0)
    p_h_n = laplace(cnt_h_n, tot_n, 2, alpha=1.0)

    _, cnt_c_y, tot_y2 = cond_prob(df, "Cloudy", "Yes", "Yes")
    _, cnt_c_n, tot_n2 = cond_prob(df, "Cloudy", "Yes", "No")
    p_c_y = laplace(cnt_c_y, tot_y2, 2, alpha=1.0)
    p_c_n = laplace(cnt_c_n, tot_n2, 2, alpha=1.0)

    num_yes = P["Yes"] * p_h_y * p_c_y
    num_no  = P["No"]  * p_h_n * p_c_n
    denom   = num_yes + num_no
    post_yes = num_yes / denom
    post_no  = num_no  / denom
    print(f"Prior P(R=Yes)={P['Yes']:.4f}, P(R=No)={P['No']:.4f}")
    print(f"P(H=High|Yes)={p_h_y:.4f}, P(C=Yes|Yes)={p_c_y:.4f}")
    print(f"P(H=High|No) ={p_h_n:.4f}, P(C=Yes|No) ={p_c_n:.4f}")
    print(f"Posterior Yes={post_yes:.4f}, No={post_no:.4f}")

    combo = (
        df.assign(RainYes=(df["Rain"]=="Yes").astype(int))
          .groupby(["Humidity","Cloudy"])["RainYes"].mean()
          .reset_index()
          .rename(columns={"RainYes":"P_Rain_Yes"})
    )
    print(combo.to_string(index=False))

    plt.figure(figsize=(7,4))
    labels = [f"{h[:1]}/{c[:1]}" for h,c in zip(combo["Humidity"], combo["Cloudy"])]
    plt.bar(labels, combo["P_Rain_Yes"].values)
    plt.title("Estimated P(Rain=Yes) by Humidity/Cloudy")
    plt.xlabel("H/C: High/Yes, High/No, Low/Yes, Low/No")
    plt.ylabel("Probability of Rain")
    plt.ylim(0,1)
    plt.tight_layout()
    plt.savefig("rain_by_humidity_cloudy.png", dpi=160)
    plt.show()
    print("Saved rain_by_humidity_cloudy.png")

if __name__ == "__main__":
    main()
