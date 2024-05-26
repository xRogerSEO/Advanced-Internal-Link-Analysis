# Import necessary libraries
import pandas as pd
import spacy
from bs4 import BeautifulSoup
import streamlit as st
import csv

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to upload and validate files
def upload_files():
    gsc_file = st.file_uploader("Upload GSC Performance Report (CSV)", type=["csv"])
    html_file = st.file_uploader("Upload Screaming Frog HTML Report", type=["html"])
    
    if gsc_file and html_file:
        gsc_df = pd.read_csv(gsc_file)
        html_content = html_file.read()
        
        # Validate GSC file columns
        required_columns = ['URL', 'Query', 'Clicks', 'Impressions', 'CTR', 'Position']
        if not all(col in gsc_df.columns for col in required_columns):
            st.error("GSC file missing required columns.")
            return None, None
        
        return gsc_df, html_content
    return None, None

# Main function to start the app
def main():
    st.title("Internal Linking Analysis and Optimization")
    
    gsc_df, html_content = upload_files()
    
    if gsc_df is not None and html_content is not None:
        # Proceed with further steps
        pass

if __name__ == "__main__":
    main()
# Function to extract links from HTML report
def extract_links_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    
    for a_tag in soup.find_all('a', href=True):
        link = {
            'href': a_tag['href'],
            'text': a_tag.get_text(strip=True)
        }
        links.append(link)
    
    return pd.DataFrame(links)

# Update main function to include link extraction
def main():
    st.title("Internal Linking Analysis and Optimization")
    
    gsc_df, html_content = upload_files()
    
    if gsc_df is not None and html_content is not None:
        links_df = extract_links_from_html(html_content)
        st.write("Links Extracted from HTML Report:")
        st.write(links_df.head())
        
        # Proceed with further steps
        pass

if __name__ == "__main__":
    main()
# Function to perform semantic analysis
def semantic_analysis(queries):
    keywords = []
    for query in queries:
        doc = nlp(query)
        for token in doc:
            if token.is_alpha and not token.is_stop:
                keywords.append(token.lemma_)
    return keywords

# Update main function to include semantic analysis
def main():
    st.title("Internal Linking Analysis and Optimization")
    
    gsc_df, html_content = upload_files()
    
    if gsc_df is not None and html_content is not None:
        links_df = extract_links_from_html(html_content)
        st.write("Links Extracted from HTML Report:")
        st.write(links_df.head())
        
        gsc_df['Keywords'] = gsc_df['Query'].apply(lambda x: semantic_analysis(x.split(',')))
        st.write("GSC Data with Keywords:")
        st.write(gsc_df.head())
        
        # Proceed with further steps
        pass

if __name__ == "__main__":
    main()
# Function to analyze internal links and provide suggestions
def analyze_internal_links(gsc_df, links_df):
    suggestions = []
    
    for index, row in gsc_df.iterrows():
        url = row['URL']
        keywords = row['Keywords']
        
        for keyword in keywords:
            for link in links_df.itertuples():
                if keyword in link.text:
                    suggestion = {
                        'Source URL': url,
                        'Target URL': link.href,
                        'Anchor Text': keyword,
                        'Suggested Context': f"Consider linking '{keyword}' from {url} to {link.href}"
                    }
                    suggestions.append(suggestion)
    
    return pd.DataFrame(suggestions)

# Update main function to include internal link analysis
def main():
    st.title("Internal Linking Analysis and Optimization")
    
    gsc_df, html_content = upload_files()
    
    if gsc_df is not None and html_content is not None:
        links_df = extract_links_from_html(html_content)
        st.write("Links Extracted from HTML Report:")
        st.write(links_df.head())
        
        gsc_df['Keywords'] = gsc_df['Query'].apply(lambda x: semantic_analysis(x.split(',')))
        st.write("GSC Data with Keywords:")
        st.write(gsc_df.head())
        
        suggestions_df = analyze_internal_links(gsc_df, links_df)
        st.write("Internal Linking Suggestions:")
        st.write(suggestions_df)
        
        # Download suggestions as CSV
        csv = suggestions_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Suggestions as CSV",
            data=csv,
            file_name='internal_linking_suggestions.csv',
            mime='text/csv'
        )

if __name__ == "__main__":
    main()
# Function to upload and validate files with error handling
def upload_files():
    gsc_file = st.file_uploader("Upload GSC Performance Report (CSV)", type=["csv"])
    html_file = st.file_uploader("Upload Screaming Frog HTML Report", type=["html"])
    
    if gsc_file and html_file:
        try:
            gsc_df = pd.read_csv(gsc_file)
            html_content = html_file.read()
        except Exception as e:
            st.error(f"Error reading files: {e}")
            return None, None
        
        # Validate GSC file columns
        required_columns = ['URL', 'Query', 'Clicks', 'Impressions', 'CTR', 'Position']
        if not all(col in gsc_df.columns for col in required_columns):
            st.error("GSC file missing required columns.")
            return None, None
        
        return gsc_df, html_content
    return None, None

# Update main function to include error handling and validation
def main():
    st.title("Internal Linking Analysis and Optimization")
    
    gsc_df, html_content = upload_files()
    
    if gsc_df is not None and html_content is not None:
        links_df = extract_links_from_html(html_content)
        st.write("Links Extracted from HTML Report:")
        st.write(links_df.head())
        
        gsc_df['Keywords'] = gsc_df['Query'].apply(lambda x: semantic_analysis(x.split(',')))
        st.write("GSC Data with Keywords:")
        st.write(gsc_df.head())
        
        suggestions_df = analyze_internal_links(gsc_df, links_df)
        st.write("Internal Linking Suggestions:")
        st.write(suggestions_df)
        
        # Download suggestions as CSV
        csv = suggestions_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Suggestions as CSV",
            data=csv,
            file_name='internal_linking_suggestions.csv',
            mime='text/csv'
        )

if __name__ == "__main__":
    main()
