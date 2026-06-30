
from tabulate import tabulate
import subprocess
from crud.patient_module.input import mandatory_field
from crud import menu_details
from crud.menu_details import menu_width


def execute_db_action(cursor, query, params=None, action='read'):
    """Handles all database execution safely using parameterized queries."""
    cursor.execute("USE hospital_manager")
    
    cursor.execute(query, params or ())

    if action == 'read':
        rows = cursor.fetchall()
        headers = cursor.column_names
        return rows, headers
    
    elif action in ('update', 'delete'):
        if cursor.rowcount == 0:
            print("\nWarning: No bill data was modified. Check your criteria.")
        else:
            print(f"\nSuccess! Modified {cursor.rowcount} bill record(s).")
        return cursor.rowcount
class CRUDBill:

    @staticmethod
    def get_bill(cursor):

        subprocess.run(["clear"])

        print("\033[3mFill in patient's data below\033[0m")
        print()

        query = '''
                select b.patient_id, concat(p.first_name, ' ' , p.last_name) as patients_name, b.bill_id, t.treatment_type, amount
                from bills b
                left join patients p on b.patient_id = p.patient_id
                left join treatments t on b.treatment_id = t.treatment_id
                left join appointments a on a.appointment_id = t.appointment_id
                where payment_status = 'Pending' and status = 'Completed' and payment_method != 'Insurance'
                '''
        # params = (f"%{patient_last_name}%", f"%{patient_first_name}%")
        
        rows, headers = execute_db_action(cursor, query)

        print("\BILL'S DATA SEARCH RESULT\n")
        if rows:
            print(tabulate(rows, headers=headers, tablefmt="grid"))
        else:
            print("No matching bill found.")

        return rows

    @staticmethod
    def print_bill(cursor, rows):
        query = '''
                select concat(p.first_name, ' ' , p.last_name) as patient_name, treatment_type, description, cost, amount, bill_date
                from bills b
                left join patients p on b.patient_id = p.patient_id
                left join treatments t on b.treatment_id = t.treatment_id
                where bill_id = %s
                '''
        
        while True:
            bill_id = mandatory_field('bill ID: ')
            valid_ids = [str(bill[2]) for bill in rows]

            if bill_id in valid_ids:
                break

            print(f"\033[31m❌ Error: ID {bill_id} is not in the search results above. Please choose a visible ID.\033[0m")
            continue

        params = (bill_id,)
        rows, headers = execute_db_action(cursor, query, params)
        result = next((dict(zip(headers, row)) for row in rows), None)

        if not result:
            print(f"\033[31m❌ Error: Bill details could not be retrieved from the database.\033[0m")
            return
        
        inner_width = menu_width - 4  

        cost_val = int(result['cost']) if result['cost'] else 0
        total_val = cost_val + 200 + 10

        #Format of the bill
        item_1 = f"1. {result['treatment_type']}".ljust(inner_width - 8) + f"${cost_val}".rjust(8)
        item_2 = "2. Consultation".ljust(inner_width - 8) + "$200".rjust(8)
        item_3 = "3. Admin Fee".ljust(inner_width - 8) + "$10".rjust(8)
        total_line = "TOTAL".ljust(inner_width - 8) + f"${total_val}".rjust(8)

        # 4. Construct the data layout with fixed 2-space side padding built-in
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

        # 5. Print out the bill frames
        print(f"╔{'═' * menu_width}╗")
        for line in data:
            print(line)
        print(f"╚{'═' * menu_width}╝")

        query_update_status = '''UPDATE bills
                                 SET payment_status = 'Paid'
                                 WHERE bill_id = %s'''
        
        params = (bill_id,)

        execute_db_action(cursor, query_update_status, params, 'update')

    def cancel_bill(cursor, rows):
        while True:
            bill_id = mandatory_field('bill ID: ')
            valid_ids = [str(bill[2]) for bill in rows]

            if bill_id in valid_ids:
                break

            print(f"\033[31m❌ Error: ID {bill_id} is not in the search results above. Please choose a visible ID.\033[0m")
            continue

        query_update_status = '''UPDATE bills
                                 SET payment_status = 'Failed'
                                 WHERE bill_id = %s'''

        params = (bill_id,)

        execute_db_action(cursor, query_update_status, params, 'update')
        print('Bill sucessfully cancelled.')

def main(conn):

    cursor = conn.cursor()

    while True:
        subprocess.run(["clear"])

        rows = CRUDBill.get_bill(cursor)

        option = menu_details.main_menu(menu_details.bill_menu_lines)
        try:
            if option == '1': #Print Bill
                print("Printing Patient's Bill...")
                CRUDBill.print_bill(cursor, rows)
            elif option == '2': #Cancel Bill
                print("Cancelling Patient's Bill...")
                CRUDBill.cancel_bill(cursor, rows)
            elif option == '3': #Back to main menu
                print('Returning to the main menu...')
                break
            else:
                print("Invalid option. Please choose 1-3.")
            
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"An error occurred: {e}")
            if conn.is_connected():
                conn.rollback()
            input("\nPress Enter to continue...")
        

