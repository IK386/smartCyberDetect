import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import plotly.express as px
import plotly.figure_factory as ff
from streamlit_autorefresh import st_autorefresh
import pickle
import streamlit as st 
accuracy = "N/A"
st.title("SmartCyberDetect Platform")
st.page_link("pages/1_AI_Detection.py", label="Start AI Detection")
st.page_link("pages/2_Request_Demo.py", label="Request Demo")
st.subheader(f"ML Model Accuracy:{accuracy}")

data = pd.read_csv("logs.txt",sep=",")
data.columns = data.columns.str.strip()
data.rename(columns={"Timestamp":"timestamp"},inplace=True
            )
print(data.columns)
data["timestamp"] = pd.to_datetime(data["timestamp"])
data["timestamp"] = data["timestamp"].astype(int)//10**9
top_attackers = data[data["status"]=="attack"]["source_ip"].value_counts()
high_risk_ips = top_attackers[top_attackers>5]
for ip, count in high_risk_ips.items():
 st.warning(f"⚠️ High-Risk Source IP {ip} with {count} attacks!")

# ===========================
# Network Activity Chart
# ===========================
st.subheader("Network Activity")
status_counts = data["status"].value_counts().reset_index()
status_counts.columns = ["status","count"]
fig_network = px.bar(
status_counts,
x="status",
y="count",
color="status",
title="Network Activity",
color_discrete_map={"normal":"green","suspicious":"orange","attack":"red"}
)
st.plotly_chart(fig_network, key="network_activity_chart")

# ===========================
# Attacks Over Time
# ===========================
st.subheader("Attacks Over Time")
attack_data = data[data["status"]=="attack"]
fig_attacks_time = px.line(
attack_data,
x="timestamp",
y="packet_size",
title="Attack Activity Over Time"
)
st.plotly_chart(fig_attacks_time, key="attacks_time_chart")

# ===========================
# IP Risk Score
# ===========================# Load data
data = pd.read_csv("logs.txt")
data = pd.read_csv("logs.txt")

# Convert timestamp to numeric value
data["timestamp"] = pd.to_datetime(data["timestamp"])
data["timestamp"] = data["timestamp"].astype(int) // 10**9

# Convert text columns to numeric values
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
data["source_ip"] = le.fit_transform(data["source_ip"])
data["dest_ip"] = le.fit_transform(data["dest_ip"])
data["protocol"] = le.fit_transform(data["protocol"])

# Features
X = data.drop("status", axis=1)

# ===========================
# Predict Future Attack
# ===========================
data["future_attack"] = data["status"].shift(-1)

data["future_attack"] = data["future_attack"].apply(lambda x: 1 if x=="attack" else 0)

data = data.dropna()

# Features
X = data.drop(["status","future_attack"], axis=1)

# Target
y = data["future_attack"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestClassifier()
model.fit(X_train, y_train)
accuracy = accuracy_score(y_test,model.predict(X_test))

with open("model.pkl","wb") as f:pickle.dump(model,f)

# Risk score
risk_scores_pred = model.predict_proba(X)[:,1]
data["risk_score"] = risk_scores_pred

risk_scores_pred = model.predict_proba(X)

st.subheader("IP Risk Score")
risk_scores_pred = model.predict_proba(X)[:,1]
# Early Warning Alert
for i, score in enumerate(risk_scores_pred):
 if score > 0.8:
  st.error(f"🚨 Predicted Attack Incoming from IP {data.iloc[i]['source_ip']} (Risk: {round(score,2)})")
data["risk_score"] = risk_scores_pred
st.dataframe(data[["source_ip","risk_score"]].sort_values(by="risk_score", ascending=False).head(10))

# ===========================
# Heatmap
# ===========================
st.subheader("Heatmap of Attacks")
heatmap_data = data.pivot_table(index="source_ip", columns="dest_ip", values="risk_score", fill_value=0)
fig_heatmap = ff.create_annotated_heatmap(
z=heatmap_data.values,
x=heatmap_data.columns.astype(str).tolist(),
y=heatmap_data.index.astype(str).tolist(),
colorscale="Reds"
)
st.plotly_chart(fig_heatmap, use_container_width=True, key="heatmap_attacks")
# ===========================
# Network Logs Table
# ===========================
st.subheader("Network Logs")
st.dataframe(data)

# ===========================
# Download Logs
# ===========================
st.subheader("Download Logs")
csv = data.to_csv(index=False)
st.download_button(
    label="Download Logs CSV",
    data=csv,
    file_name="network_logs.csv",
    mime="text/csv",
)
if st.button("Start AI Detection"):
    st.switch_page("pages/1_AI_Detection.py")

if st.button("Request Demo"):
    st.switch_page("pages/2_Request_Demo.py")