mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]\n\
primaryColor = '#933252'\n\
backgroundColor = '#0e1117'\n\
secondaryBackgroundColor = '#31333f'\n\
textColor = '#FFFFFF'\n\
font = ‘sans serif’\n\
" > ~/.streamlit/config.toml
