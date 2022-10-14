mkdir -p ~/.streamlit/

echo '[theme]
primaryColor="#edcf94"
backgroundColor="#f9f0d5"
secondaryBackgroundColor="#f0e6d6"
textColor="#314448"
font="monospace"

[server]
runOnSave = true
'> ~/.streamlit/config.toml


cd "`dirname "$0"`"

streamlit run streamlit.py
