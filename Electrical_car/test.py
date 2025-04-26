import streamlit as st
from ev_report import EVReportGenerator

st.set_page_config(page_title="EV Market Report", layout="wide")
st.title("🔋 Electric Vehicle Market Intelligence Report Generator")

query = st.text_input("🔍 Enter your query:",
                      "Generate a strategy intelligence report for the electric vehicle market and its key players.")

if st.button("🚀 Generate Report"):
    with st.spinner("Generating report... Please wait."):
        generator = EVReportGenerator(query)
        report, logs = generator.generate_report()

    # Show logs if any
    if logs:
        st.warning("⚠️ Some warnings or errors occurred during generation:")
        for log in logs:
            st.code(log)

    # Show final report
    st.success("✅ Report Generated!")
    st.markdown(report)
