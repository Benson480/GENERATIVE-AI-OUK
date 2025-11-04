import streamlit as st
import requests
import os
import json

st.title("Codebase Genius — Demo")

repo_url = st.text_input("Public GitHub repo URL", value="https://github.com/psf/requests")
if st.button("Generate docs"):
    if not repo_url:
        st.error("Enter a repository URL")
    else:
        # call Jac backend via HTTP walker endpoint (example: http://localhost:8000/walkers/http_api)
        jac_endpoint = st.text_input("Jac server endpoint (example http://localhost:8000/walkers/http_api)", value="http://localhost:8000/walkers/http_api")
        payload = {"repo_url": repo_url}
        try:
            resp = requests.post(jac_endpoint, json={"repo_url": repo_url})
            if resp.status_code == 200:
                st.success("Request accepted — backend started processing.")
                st.write("Check outputs/ for generated docs (server writes there).")
            else:
                st.error(f"Backend returned {resp.status_code}: {resp.text}")
        except Exception as e:
            st.error(f"Failed to reach Jac server: {e}")

st.markdown("---")
st.markdown("Outputs folder path: `./outputs`")
