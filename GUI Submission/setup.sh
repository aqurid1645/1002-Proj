mkdir -p ~/.streamlit/

echo '[theme]
primaryColor="#d33682"
backgroundColor="#002b36"
secondaryBackgroundColor="#586e75"
textColor="#fafafa"
font="sans serif"

[server]
runOnSave = true
'> ~/.streamlit/config.toml


cd "`dirname "$0"`"

streamlit run Home_Page.py
