import streamlit as st
import pandas as pd

@st.cache_data
def load_rules():
    df = pd.read_csv('association_rules.csv')
    df['antecedents'] = df['antecedents'].apply(eval)
    df['consequents'] = df['consequents'].apply(eval)
    return df

rules = load_rules()

def recommend_from_rules(user_items, rules_df, top_n=5):
    recommendations = []
    for _, row in rules_df.iterrows():
        if set(row['antecedents']).issubset(user_items):
            for item in row['consequents']:
                if item not in user_items and item not in recommendations:
                    recommendations.append(item)
        if len(recommendations) >= top_n:
            break
    return recommendations

st.title("Association Rule Based Recommender")
st.write("Enter user features (comma separated), e.g.:")
st.write("`price_bin_cheap, weight_bin_light, freight_bin_low, payment_type_credit_card`")
st.markdown("**Tip:** Use exact feature names from the dataset.")

user_input = st.text_input("User's current items/features:")

if st.button('Get Recommendations'):
    if user_input:
        user_items = [item.strip() for item in user_input.split(',')]
        recs = recommend_from_rules(user_items, rules, top_n=5)
        if recs:
            st.success("Recommendations found! Here are some suggestions:")
            # Display recommendations as colored tags
            tags_html = ""
            for r in recs:
                tags_html += f'<span style="display:inline-block; background-color:#4CAF50; color:white; padding:5px 12px; border-radius:15px; margin:4px;">{r}</span>'
            st.markdown(tags_html, unsafe_allow_html=True)
        else:
            st.error("No recommendations found for this input.")
    else:
        st.error("Please enter some features/items.")
