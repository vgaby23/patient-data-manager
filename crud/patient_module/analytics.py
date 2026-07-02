import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import subprocess
from crud import menu_details
from sqlalchemy import text 
from crud.patient_module.input import mandatory_field

# Run SQL query into dataframe
def run_sql(query, conn):
    df = pd.read_sql_query(text(query), conn)
    return df

# Add labels to charts
def add_labels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha='center') 

class Analytics:

    @staticmethod
    def appointment_analysis(conn):
        # Appointment status distribution
        query = """
                SELECT status AS status_distribution,
                COUNT(*) AS total_count
                FROM appointments
                GROUP BY status
                """
        
        df = run_sql(query, conn)

        plt.figure()
        plt.pie(df['total_count'], 
                labels=df['status_distribution'],
                autopct='%1.1f%%',
                startangle=90)
        plt.title('Appointment Status Distribution')
        plt.show()
        plt.close('all')

        input('Press enter to see next chart..')

        # Monthly appointment volume & no-show rates
        query = """
                SELECT DATE_FORMAT(appointment_date, '%m') AS month,
                    COUNT(*) AS total_appointments,
                    SUM(CASE WHEN LOWER(TRIM(status)) = 'no-show' THEN 1 ELSE 0 END) AS no_show_count,
                    ROUND(SUM(CASE WHEN LOWER(TRIM(status)) = 'no-show' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS percentage_no_show
                FROM appointments
                GROUP BY month
                ORDER BY month ASC
                """
        df = run_sql(query, conn)

        # Calculate successful appointments for stacking
        attended = [t - n for t, n in zip(df['total_appointments'], df['no_show_count'])]

        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Primary Axis: Stacked Bars for volume
        ax1.bar(df['month'], attended, label='Attended', color='#4f81bd')
        ax1.bar(df['month'], df['no_show_count'], bottom=attended, label='No-Show', color='#c0504d')
        ax1.set_ylabel('Number of Appointments', color='black')
        ax1.set_xlabel('Month')
        ax1.legend(loc='upper left')
        ax1.grid(axis='y', linestyle='--', alpha=0.5)
        for container in ax1.containers:
            ax1.bar_label(container)
        # Secondary Axis: Line for Percentage Rate
        ax2 = ax1.twinx()
        ax2.plot(df['month'], df['percentage_no_show'], color='#e36c09', marker='o', linewidth=2.5, label='No-Show %')
        ax2.set_ylabel('No-Show Rate (%)', color='#e36c09')
        ax2.tick_params(axis='y', labelcolor='#e36c09')
        ax2.legend(loc='upper right')
        for container in ax2.containers:
            ax2.bar_label(container)
        plt.title('Monthly Appointment Volumes vs. No-Show Rates')
        plt.show()
        plt.close('all')

        input('Press enter to see next chart..')

        # Clinic growth
        query = """
                with
                first_visit as 
                    (select patient_id, min(appointment_date) as first_visit
                    from appointments 
                    group by patient_id)
                select *, date_format(appointment_date, '%m') as month_appointment,
                    case when appointment_date = first_visit then 'New Patient' else 'Returning Patient'
                    end as patient_type
                from appointments a
                join first_visit fv on a.patient_id = fv.patient_id
                """
        df = run_sql(query, conn)

        monthly_retention = (df.groupby(['month_appointment', 'patient_type'])
                            .size()
                            .unstack(fill_value=0))

        
        monthly_retention.index = monthly_retention.index.astype(str)

        # Plot the Stacked Area Chart
        colors = ['#2ca02c', '#1f77b4'] # Green for New, Blue for Returning
        ax = monthly_retention.plot(kind='area', stacked=True, figsize=(12, 6), color=colors, alpha=0.8)
        for container in ax.containers:
            ax.bar_label(container)
        plt.title('Hospital Growth: New vs. Returning Patients Month-over-Month')
        plt.xlabel('Month')
        plt.ylabel('Total Number of Appointments')
        plt.legend(title='Patient Type', loc='upper left')
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()
        plt.close('all')

    @staticmethod
    def financial_revenue(conn):
        query = """
            SELECT 
                payment_status,
                COUNT(bill_id) AS total_bills
            FROM bills
            GROUP BY payment_status
            HAVING COUNT(bill_id) > 10
            ORDER BY total_bills DESC;
            """
        df = run_sql(query, conn)

        plt.figure()
        plt.pie(df['total_bills'], 
                labels=df['payment_status'],
                autopct='%1.1f%%',
                startangle=90)
        plt.title('Bills per payment status')
        plt.show()
        plt.close('all')

        input('Press enter to see next chart..')

        query = """
                SELECT 
                    d.doctor_id,
                    d.first_name,
                    d.last_name,
                    d.specialization,
                    DATE_FORMAT(treatment_date, '%m') AS month,
                    SUM(t.cost) AS total_treatment_cost,
                    COUNT(t.treatment_id) AS number_of_treatments
                FROM doctors d
                JOIN appointments a ON d.doctor_id = a.doctor_id
                JOIN treatments t ON a.appointment_id = t.appointment_id
                JOIN bills b on b.treatment_id = t.treatment_id
                WHERE b.payment_status = 'Paid'
                GROUP BY d.doctor_id, month
                ORDER BY month ASC;
                """
        df = run_sql(query, conn)
        df['doctor_name'] = df['first_name'] + ' ' + df['last_name']

        # Doctor revenue heatmap across months
        heatmap_data = df.pivot(index='doctor_name', columns='month', values='total_treatment_cost')

        plt.figure(figsize=(12, 8))
        ax = sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=.5)
        for container in ax.containers:
            ax.bar_label(container)
        plt.title('Doctor Revenue Heatmap across Months ($)')
        plt.xlabel('Month')
        plt.ylabel('Doctor')
        plt.tight_layout()
        plt.show()
        plt.close('all')

        input('Press enter to see next chart..')

        heatmap_data_2 = df.pivot_table(index='specialization', columns='month', values='total_treatment_cost', aggfunc='sum')

        # Specialization revenue heatmap across months
        plt.figure(figsize=(12, 8))
        ax = sns.heatmap(heatmap_data_2, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=.5)
        for container in ax.containers:
            ax.bar_label(container)
        plt.title('Specialization Revenue Heatmap across Months ($)')
        plt.xlabel('Month')
        plt.ylabel('Specialization')
        plt.tight_layout()
        plt.show()
        plt.close('all')

        input('Press enter to see next chart..')

        # Top Performing doctors over the year
        top_doctors = (df.groupby('doctor_name')['total_treatment_cost']
                    .sum()
                    .reset_index()
                    .sort_values(by='total_treatment_cost', ascending=False))

        plt.figure(figsize=(10, 6))
        ax = sns.barplot(
            data=top_doctors, 
            x='total_treatment_cost', 
            y='doctor_name'
        )
        for container in ax.containers:
            ax.bar_label(container)
        plt.title('Top Performing Doctors Over the Year (By Total Revenue)')
        plt.xlabel('Total Revenue Generated ($)')
        plt.ylabel('Doctor Name')
        plt.tight_layout()
        plt.show()
        plt.close('all')

    @staticmethod 
    def demographics(conn):
        # Patient Age distribution by Department 
        query = """
                select p.*, specialization, date_format(now(), '%Y') - date_format(date_of_birth, '%Y') as age
                from patients p
                join appointments a on a.patient_id = p.patient_id
                join doctors d on a.doctor_id = d.doctor_id
                """
        df = run_sql(query, conn)

        plt.figure(figsize=(12, 6))
        ax = sns.boxplot(
            data=df, 
            x='specialization', 
            y='age'
        )
        
        plt.title('Patient Age Distribution by Department')
        plt.xlabel('Medical Department')
        plt.ylabel('Patient Age')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        plt.close('all')

        input('Press Enter to see next chart')
        # Age Distribution by department

        plt.figure(figsize=(12, 6))
        ax = sns.barplot(
            data=df, 
            x='specialization', 
            y='patient_id', 
            hue='gender', 
            palette={'F': '#ff99cc', 'M': '#66b3ff'}
        )
        for container in ax.containers:
            ax.bar_label(container)
        plt.title('Patient Gender Distribution by Medical Department', fontsize=14)
        plt.xlabel('Specialization', fontsize=12)
        plt.ylabel('Number of Unique Patients', fontsize=12)
        plt.xticks(rotation=0)
        plt.legend(title='Gender', loc='upper right')
        plt.grid(axis='y', linestyle='--', alpha=0.4)
        plt.tight_layout()
        plt.show()
    
    def descriptive(conn):
        """
        Function to calculate and display selected descriptive statistics 
        metrics for a given column based on user input.
        """

        query = """
                select date_format(now(), '%Y') - date_format(date_of_birth, '%Y') as age, t.cost as revenue
                from patients p 
                join appointments a on p.patient_id = a.patient_id
                join treatments t on a.appointment_id = t.appointment_id
                where a.status not in ('No-Show', 'Cancelled')
                """
        
        df = run_sql(query, conn)
        opt_list = {'1': 'Age', '2': 'Revenue'}
        while True:
                print('Available column:')
                for key, value in opt_list.items():
                    print(f'{key}: {value}')
                
                column_input = mandatory_field('Choose column to analyze(1-2): ').strip()
                if column_input not in ('1', '2'):
                    print("\033[31m❌ Value is invalid! Choose value between 1 to 2\033[0m")
                    continue
                else:
                    break
        column_name = opt_list[column_input].lower()
        
        print("\nAvailable metrics: mean, median, min, max, std, sum")
        user_metric = input("👉 Type the metric you want to compute  : ")
        
        # Calculate metric based on user selection
        if user_metric in ['mean', 'average']:
            result = df[column_name].mean()
            label = "Average (Mean)"
        elif user_metric == 'median':
            result = df[column_name].median()
            label = "Middle Value (Median)"
        elif user_metric == 'min':
            result = df[column_name].min()
            label = "Minimum Value (Min)"
        elif user_metric == 'max':
            result = df[column_name].max()
            label = "Maximum Value (Max)"
        elif user_metric in ['std', 'standard deviation']:
            result = df[column_name].std()
            label = "Standard Deviation"
        elif user_metric in ['sum', 'total']:
            result = df[column_name].sum()
            label = "Total (Sum)"
        else:
            print(f"\n❌ Error: Metric '{user_metric}' is unrecognized. Please choose a valid option (mean, median, etc.).\n")
            return

        print("\n" + "="*45)
        print("🛠️  INTERACTIVE STATISTICAL ANALYSIS MENU")
        print("="*45)


        # Print out the results beautifully formatted
        print(f"\n======================================")
        print(f"📊 DESCRIPTIVE STATISTICS REPORT")
        print(f"======================================")
        print(f"Selected Column : '{column_name}'")
        print(f"{label.ljust(22)}: {result:.2f}")
        print(f"======================================\n")


def main(conn):
    
    conn.execute(text('USE hospital_manager'))

    while True:
        subprocess.run(["clear"])

        option = menu_details.main_menu(menu_details.analytics_menu_lines)
        try:
            if option == '1': # Operational & Scheduling
                Analytics.appointment_analysis(conn)
            elif option == '2': # Financial & Revenue
                Analytics.financial_revenue(conn)
            elif option == '3': # Patient Demographics
                Analytics.demographics(conn)
            elif option == '4':  # Descriptive Analytics
                Analytics.descriptive(conn)
            elif option == '5': # Back to main menu
                print('Returning to the main menu...')
                break
            else:
                print("Invalid option. Please choose 1-4.")
            
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"An error occurred: {e}")
            
            if not conn.closed:
                conn.rollback()
            input("\nPress Enter to continue...")