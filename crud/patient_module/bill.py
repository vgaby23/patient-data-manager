from tabulate import tabulate
import subprocess
from crud.patient_module.input import mandatory_field
from crud import menu_details
from crud.menu_details import menu_width
from sqlalchemy import text

def execute_db_action(conn, query, params=None, action='read'):
    #Establish connection
    conn.execute(text("USE hospital_manager"))
    result = conn.execute(text(query), params or {})

     # Breakdown how to fetch the data based on the type of action
    if action == 'read':
        rows = result.fetchall()
        headers = list(result.keys())
        return rows, headers
    
    elif action in ('update', 'delete'):
        if result.rowcount == 0:
            print("\nWarning: No bill data was modified. Check your criteria.")
        else:
            print(f"\nSuccess! Modified {result.rowcount} bill record(s).")
        return result.rowcount


class CRUDBill:

    @staticmethod
    def get_bill(conn):

        query = '''
                select b.patient_id, concat(p.first_name, ' ' , p.last_name) as patients_name, b.bill_id, t.treatment_type, amount
                from bills b
                left join patients p on b.patient_id = p.patient_id
                left join treatments t on b.treatment_id = t.treatment_id
                left join appointments a on a.appointment_id = t.appointment_id
                where payment_status = 'Pending' and status = 'Completed' and payment_method != 'Insurance'
                '''
        
        rows, headers = execute_db_action(conn, query)

        print("\nBILL'S DATA SEARCH RESULT\n")
        if rows:
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No matching bill found.")

        return rows

    @staticmethod
    def print_bill(conn, rows):
        
        query = '''
                select concat(p.first_name, ' ' , p.last_name) as patient_name, treatment_type, description, cost, amount, bill_date
                from bills b
                left join patients p on b.patient_id = p.patient_id
                left join treatments t on b.treatment_id = t.treatment_id
                where bill_id = :bill_id
                '''
        
        # Bill ID validation
        while True:
            bill_id = mandatory_field('bill ID: ')
            valid_ids = [str(bill[2]) for bill in rows]

            if bill_id in valid_ids:
                break

            print(f"\033[31m❌ Error: ID {bill_id} is not in the search results above. Please choose a visible ID.\033[0m")

        params = {"bill_id": bill_id}
        rows_data, headers = execute_db_action(conn, query, params)
        result = next((dict(zip(headers, row)) for row in rows_data), None)

        if not result:
            print(f"\033[31m❌ Error: Bill details could not be retrieved from the database.\033[0m")
            return
        
        inner_width = menu_width - 4  

        cost_val = int(result['cost']) if result['cost'] else 0
        total_val = cost_val + 200 + 10

        # Format of the printed bill
        item_1 = f"1. {result['treatment_type']}".ljust(inner_width - 8) + f"${cost_val}".rjust(8)
        item_2 = "2. Consultation".ljust(inner_width - 8) + "$200".rjust(8)
        item_3 = "3. Admin Fee".ljust(inner_width - 8) + "$10".rjust(8)
        total_line = "TOTAL".ljust(inner_width - 8) + f"${total_val}".rjust(8)

        data = [
            f"║{' ':^{menu_width}}║",
            f"║{'BILL':^{menu_width}}║",
            f"║{' ':^{menu_width}}║",
            f"║{'=' * menu_width}║",
            f"║{' ':^{menu_width}}║",
            f"║  {f'Patient: {result['patient_name']}':<{inner_width}}  ║",
            f"║  {f'Date: {result['bill_date']}':<{inner_width}}  ║",
            f"║{' ':^{menu_width}}║",
            f"║{'=' * menu_width}║",
            f"║  {item_1:<{inner_width}}  ║",
            f"║  {item_2:<{inner_width}}  ║",
            f"║  {item_3:<{inner_width}}  ║",
            f"║{'=' * menu_width}║",
            f"║{' ':^{menu_width}}║",
            f"║  {total_line:<{inner_width}}  ║",
            f"║{' ':^{menu_width}}║"
        ]
        subprocess.run(["clear"])
        
        print(f"╔{'═' * menu_width}╗")
        for line in data:
            print(line)
        print(f"╚{'═' * menu_width}╝")

        
        query_update_status = '''UPDATE bills
                                 SET payment_status = 'Paid'
                                 WHERE bill_id = :bill_id'''
        
        execute_db_action(conn, query_update_status, params, 'update')

    @staticmethod
    def cancel_bill(conn, rows):
        while True:
            bill_id = mandatory_field('bill ID: ')
            valid_ids = [str(bill[2]) for bill in rows]

            if bill_id in valid_ids:
                break

            print(f"\033[31m❌ Error: ID {bill_id} is not in the search results above. Please choose a visible ID.\033[0m")

        query_update_status = '''UPDATE bills
                                 SET payment_status = 'Failed'
                                 WHERE bill_id = :bill_id'''

        
        params = {"bill_id": bill_id}

        execute_db_action(conn, query_update_status, params, 'update')
        print('Bill successfully cancelled.')

def main(conn):
    
    while True:

        subprocess.run(["clear"])
        rows = CRUDBill.get_bill(conn)

        option = menu_details.main_menu(menu_details.bill_menu_lines)
        try:
            if option == '1': #Print Bill
                print("Printing Patient's Bill...")
                CRUDBill.print_bill(conn, rows)
                conn.commit() # 
            elif option == '2': #Cancel Bill
                print("Cancelling Patient's Bill...")
                CRUDBill.cancel_bill(conn, rows)
                conn.commit() # 
            elif option == '3': #Back to main menu
                print('Returning to the main menu...')
                break
            else:
                print("Invalid option. Please choose 1-3.")
            
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"An error occurred: {e}")
            
            if not conn.closed:
                conn.rollback()
            input("\nPress Enter to continue...")