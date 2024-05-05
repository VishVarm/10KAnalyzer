from sec_edgar_downloader import Downloader


#Create new downloader, dl, and save stock data
dl = Downloader("VishnuVarmaCodingCompany", "vishvarm04@gmail.com")

# Download 10-K documents for Zoom from 1995 through 2023
dl.get("10-K", "ZM", after="1995-01-01", before="2023-12-31")
# Download 10-K documents for Pfizer from 1995 through 2023
dl.get("10-K", "PFE", after="1995-01-01", before="2023-12-31")


