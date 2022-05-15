from ctypes import alignment
from fpdf import FPDF
from importlib.resources import path
import pandas as pd
from pandas import DataFrame
from create_table_fpdf2 import PDF


# Pulls data from spreadsheet
# Insert the correct spreadsheet here
guild_table = pd.read_excel('BTF Guild Management - Cycle End 2022.05.13.xlsx', 'Billing')

# Insert Start Date Here
start_date = "April 29th, 2022"
end_date = "May 13th, 2022"

# print(guild_table["Landlord"])
landlords = []
for name in guild_table["Landlord"]:

    if landlords == None:
        landlords.append(name)
    elif name not in landlords:
        landlords.append(name)
        

for name in landlords:
    specific_landlord = guild_table[guild_table['Landlord'] == name]
    cedalion_list = []
    plot_list = []
    lava_earned_list = []
    lava_donation_percent_list = []
    lava_donation_total_list = []
    total_due = 0
    
    for i, row in specific_landlord.iterrows():
        
        plot_number = str(row['Plot Number'])
        plot_number_no_dec = plot_number.split(".", 1)[0]

        lava_donation_percent = row['Lava Donating Percentage'] * 100
        lava_donation_with_percentage = str(lava_donation_percent) + '%'

        cedalion_list.append(row['Rentee'])
        plot_list.append(plot_number_no_dec)
        lava_earned_list.append(str(row['Lava Earned']))
        lava_donation_percent_list.append(lava_donation_with_percentage)
        lava_donation_total_list.append(str(row['Lava Donation Total']))
        total_due = total_due + row['Lava Donation Total']

    df = {
        'Rentee': cedalion_list,
        'Plot Number': plot_list,
        'Lava Earned': lava_earned_list,
        'Lava Donating Percentage': lava_donation_percent_list,
        'Lava Donation Total': lava_donation_total_list
        }

    # Will change this to be customized for each PDF generated
    title = 'INVOICE'
    title2 = 'BTF Cedalion Guild'
        

    pdf = PDF('P', 'mm', 'Letter')
    pdf.add_page()

    # Header on first page
    pdf.set_text_color(0,0,0)
    pdf.set_font('times', '', 10)
    pdf.text(47, 30, 'Below indicates the $LAVA earned on Cedalion plots '
    'allocated to the BTF guild')
    pdf.text(75, 38, f'Dates: {start_date} to {end_date}')
    pdf.text(83, 48, 'Please send to wallet address:')
    pdf.text(65, 53, '0xd81D7907D603Eed8D8a557d8164D27A3a1F49505')

    pdf.set_text_color(0,0,0)
    pdf.set_font('courier', 'B', 22)

    # Puts in the total Lava
    total_due = "{:.2f}".format(total_due)
    pdf.text(93, 70, f'Total LAVA due: {total_due}')

    pdf.create_table(
        table_data = df, 
        title=f'Invoice to: {name}',
        x_start=13,
        align_header='C',
        align_data='C',
        emphasize_data=[f'{name}'],
        emphasize_style='BIU')

    pdf.ln()
    pdf.set_fill_color(255, 140, 0)
    pdf.set_text_color(255,255,255)
    pdf.set_font('times', 'B', 20)
    pdf.cell(0, 10, 
    txt='Thank you for your contribution!', 
    ln=1, 
    align='C', 
    fill=1
    )

    pdf.output(f'{name}_btf_invoice.pdf')
