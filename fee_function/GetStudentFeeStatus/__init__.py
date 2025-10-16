import azure.functions as func
import datetime, pyodbc, os

def main(req: func.HttpRequest) -> func.HttpResponse:
    student_id = req.params.get("StudentID")
    if not student_id:
        return func.HttpResponse("Provide StudentID", status_code=400)

    try:
        conn = pyodbc.connect(os.environ["SQL_CONNECTION"])
        cursor = conn.cursor()
        cursor.execute("SELECT TotalFee, PaidAmount, DueDate FROM Students WHERE StudentID=?", student_id)
        row = cursor.fetchone()
        if not row:
            return func.HttpResponse("Student not found", status_code=404)

        total, paid, due = row
        today = datetime.date.today()
        if paid >= total:
            status = "Paid"
        elif due < today:
            status = "Overdue"
        else:
            status = "Partially Paid"
        return func.HttpResponse(status)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)
