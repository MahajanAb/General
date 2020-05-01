def calculator(company_data):
    #these variables are only mentioned in the formula section of the document. So it's not clear, where these values come from.
    #total_assets = 
    # #total_liabilities =             
    X1 = (company_data.total_current_assets - company_data.total_current_liabilities) #/ total_assets            
    X2 = company_data.retained_earnings #/ total_assets 
    X3 = company_data.earnings_before_interest_taxes #/ total_assets 
    X4 = company_data.book_value_equity #/ total_liabilities

    company_data.BRS = 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4

    if company_data.BRS > 2.6:
        company_data.BRZ = "Green"
    elif 2.6 >= company_data.BRS and company_data.BRS > 1.1:
        company_data.BRZ = "Yellow"
    elif 1.1 >= company_data.BRS:
        company_data.BRZ = "Red"
         
    return [company_data.BRS, company_data.BRZ]