import streamlit as st
import pandas as pd
from supabase import create_client, Client  # ✅ This is correct
import datetime



# 🌐 Supabase setup
SUPABASE_URL = "https://ytmnnylyerotfvkizumn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl0bW5ueWx5ZXJvdGZ2a2l6dW1uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg5MTkxNzgsImV4cCI6MjA2NDQ5NTE3OH0.GkQqZvTo5JFazjBljqfjeXLmj5P3bIBlbO6ejdSaiyw"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

import streamlit as st
import datetime

# Make sure you initialize your Supabase client somewhere before using it
# from supabase import create_client
# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="H.E.A.R.T Project", layout="centered")

# Sidebar menu to navigate pages
page = st.sidebar.selectbox("Choose a page", [
    "Home",
    "Register Child",
    "Attendance",
    "Reports",
    "Performance",
    "Profile",
    "Edit Profile"
])

def home():
    st.markdown(
        """
        <style>
            .title {
                text-align: center;
                font-size: 60px;
                font-weight: 900;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #d63384;
                margin-bottom: 10px;
            }
            .heart-emoji {
                text-align: center;
                font-size: 80px;
                margin-top: 0;
                margin-bottom: 30px;
            }
            .motto {
                text-align: center;
                font-style: italic;
                font-size: 22px;
                color: #555;
                margin-bottom: 20px;
            }
            .verse {
                text-align: center;
                font-style: italic;
                font-size: 20px;
                color: #666;
                line-height: 1.6;
            }
        </style>

        <div class="title">H.E.A.R.T.</div>
        <div class="heart-emoji">💖</div>
        <div class="motto">
            Held — Embraced — Accepted — Remembered — Treasured
        </div>
        <div class="verse">
            “I have loved you with an everlasting love;<br>
            therefore I have continued my faithfulness to you.”<br>
            — Jeremiah 31:3
        </div>
        """,
        unsafe_allow_html=True
    )

import datetime  # Add this at the top of your script if not already present

import datetime
import streamlit as st

import streamlit as st
import datetime

def register_child():
    st.title("📝 Register a Child")

    with st.form("register_form"):
        col1, col2 = st.columns(2)

        with col1:
            first_name = st.text_input("First Name")
            birthdate = st.date_input(
                "Birthdate",
                min_value=datetime.date(1900, 1, 1),
                max_value=datetime.date.today()
            )
            grade = st.selectbox("Grade", ["PP1", "PP2", "1", "2", "3", "4", "5", "6", "7", "8"])
            group_class = st.selectbox("Group/Class", ["Angels", "Stars", "Warriors", "Champions"])
            school = st.text_input("School")
            
            # Calculate age
            today = datetime.date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        with col2:
            last_name = st.text_input("Last Name")
            location = st.text_input("Location")
            guardian_name = st.text_input("Guardian Name")
            guardian_contact = st.text_input("Guardian Contact")

        submitted = st.form_submit_button("Register Child")

        if submitted:
            if first_name and last_name and guardian_name:
                full_name = f"{first_name} {last_name}"
                try:
                    response = supabase.table("children").insert({
                        "full_name": full_name,
                        "age": age,
                        "birthdate": birthdate.isoformat(),
                        "grade": grade,
                        "school": school,
                        "location": location,
                        "group_class": group_class,
                        "guardian_name": guardian_name,
                        "guardian_contact": guardian_contact
                    }).execute()

                    if response.data:
                        st.success(f"🎉 {full_name} has been registered successfully!")
                    else:
                        st.error("⚠️ Registration failed. No data returned.")

                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.warning("Please fill in the required fields (First Name, Last Name, Guardian).")


def attendance():
    st.markdown("""
    <style>
        .attendance-title {
            color: #008080;
            text-align: center;
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .section-label {
            color: #004d4d;
            font-size: 1.1em;
            font-weight: 500;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="attendance-title">📅 Mark Attendance</div>', unsafe_allow_html=True)

    today = datetime.date.today()
    attendance_date = st.date_input("Select attendance date", max_value=today)

    groups_response = supabase.table("children").select("group_class").neq("group_class", "").execute()
    groups = sorted({row['group_class'] for row in groups_response.data}) if groups_response.data else []

    if not groups:
        st.warning("⚠️ No groups found. Please register children first.")
        return

    group = st.selectbox("Select Group/Class", groups)

    children_response = supabase.table("children").select("id, full_name").eq("group_class", group).execute()
    children_list = children_response.data or []

    if not children_list:
        st.info(f"No children registered in group '{group}'.")
        return

    st.markdown(f"### 👥 Mark attendance for {len(children_list)} children in **{group}**")

    attendance_response = supabase.table("attendance") \
        .select("child_id, present") \
        .eq("attendance_date", attendance_date.isoformat()) \
        .execute()

    attendance_records = {rec['child_id']: rec['present'] for rec in attendance_response.data} if attendance_response.data else {}

    with st.form("attendance_form"):
        present_dict = {}
        for child in children_list:
            checked = attendance_records.get(child['id'], False)
            present_dict[child['id']] = st.checkbox(child['full_name'], value=checked, key=f"present_{child['id']}")

        submitted = st.form_submit_button("✅ Save Attendance")

        if submitted:
            for child_id, present in present_dict.items():
                existing = supabase.table("attendance").select("id") \
                    .eq("child_id", child_id) \
                    .eq("attendance_date", attendance_date.isoformat()) \
                    .execute()

                if existing.data:
                    supabase.table("attendance").update({"present": present}) \
                        .eq("id", existing.data[0]['id']) \
                        .execute()
                else:
                    supabase.table("attendance").insert({
                        "child_id": child_id,
                        "attendance_date": attendance_date.isoformat(),
                        "present": present
                    }).execute()

            st.success("✅ Attendance saved successfully!")





import pandas as pd
import calendar

def reports():
    st.markdown("<h2 style='color:#ff69b4;'>📊 Attendance Reports</h2>", unsafe_allow_html=True)

    report_type = st.selectbox("Select report type", ["Daily", "Monthly", "Yearly"])
    
    # Fetch groups for filtering
    groups_response = supabase.table("children").select("group_class").neq("group_class", "").execute()
    groups = list({row['group_class'] for row in groups_response.data}) if groups_response.data else []
    groups.sort()
    groups.insert(0, "All Groups")

    selected_group = st.selectbox("Filter by Group/Class", groups)

    if report_type == "Daily":
        date = st.date_input("Select date", value=datetime.date.today())
    elif report_type == "Monthly":
        year = st.number_input("Select Year", min_value=2000, max_value=datetime.date.today().year, value=datetime.date.today().year)
        month = st.selectbox("Select Month", list(calendar.month_name)[1:])
    else:  # Yearly
        year = st.number_input("Select Year", min_value=2000, max_value=datetime.date.today().year, value=datetime.date.today().year)

    # Query attendance data based on report type
    query = supabase.table("attendance").select("child_id, attendance_date, present")

    if selected_group != "All Groups":
        # Get child IDs in the group
        children_resp = supabase.table("children").select("id, full_name").eq("group_class", selected_group).execute()
        child_ids = [child['id'] for child in children_resp.data] if children_resp.data else []
        if not child_ids:
            st.warning(f"No children found in group {selected_group}")
            return
        query = query.in_("child_id", child_ids)

    # Filter dates
    if report_type == "Daily":
        query = query.eq("attendance_date", date.isoformat())
    elif report_type == "Monthly":
        start_date = datetime.date(year, list(calendar.month_name).index(month), 1)
        if month == "December":
            end_date = datetime.date(year+1, 1, 1) - datetime.timedelta(days=1)
        else:
            end_date = datetime.date(year, list(calendar.month_name).index(month)+1, 1) - datetime.timedelta(days=1)
        query = query.gte("attendance_date", start_date.isoformat()).lte("attendance_date", end_date.isoformat())
    else:  # Yearly
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year, 12, 31)
        query = query.gte("attendance_date", start_date.isoformat()).lte("attendance_date", end_date.isoformat())

    attendance_data_resp = query.execute()
    attendance_data = attendance_data_resp.data or []

    if not attendance_data:
        st.info("No attendance data found for the selected filters.")
        return

    # Create a DataFrame for display
    # Get child names from child_id
    child_ids = list(set([record['child_id'] for record in attendance_data]))
    children_resp = supabase.table("children").select("id, full_name").in_("id", child_ids).execute()
    id_to_name = {child['id']: child['full_name'] for child in children_resp.data} if children_resp.data else {}

    rows = []
    for record in attendance_data:
        rows.append({
            "Child Name": id_to_name.get(record['child_id'], "Unknown"),
            "Date": record['attendance_date'],
            "Present": "Yes" if record['present'] else "No"
        })

    df = pd.DataFrame(rows)

    st.dataframe(df.style.applymap(lambda v: 'background-color: #d1f7c4' if v == "Yes" else 'background-color: #f7c4c4', subset=['Present']))

def performance():
    st.markdown("<h2 style='color:#ff69b4;'>📚 Record & View Performance</h2>", unsafe_allow_html=True)

    # Step 1: Fetch available group_classes
    groups_response = supabase.table("children").select("group_class").neq("group_class", "").execute()
    groups = sorted(list({child['group_class'] for child in groups_response.data})) if groups_response.data else []

    if not groups:
        st.warning("No groups found. Please register children first.")
        return

    selected_group = st.selectbox("Select Group/Class", groups)

    # Step 2: Fetch children in the selected group
    children_response = supabase.table("children").select("id, full_name").eq("group_class", selected_group).execute()
    children_list = children_response.data or []

    if not children_list:
        st.warning("No children found in this group.")
        return

    # Step 3: Select child
    child_names = {child['full_name']: child['id'] for child in children_list}
    selected_name = st.selectbox("Select Child", list(child_names.keys()))
    selected_id = child_names[selected_name]

    st.markdown("### ✍️ Add New Performance Record")

    with st.form("performance_form"):
        subject = st.text_input("Subject", max_chars=50)
        score = st.number_input("Score (0–100)", min_value=0, max_value=100, step=1)
        term = st.text_input("Term (e.g. Term 1, 2025)", max_chars=50)
        comments = st.text_area("Comments (optional)", height=100)

        submit = st.form_submit_button("Save Performance")

        if submit:
            if subject.strip() == "" or term.strip() == "":
                st.error("Subject and Term are required fields.")
            else:
                new_record = {
                    "child_id": selected_id,
                    "subject": subject.strip(),
                    "score": score,
                    "term": term.strip(),
                    "comments": comments.strip()
                }
                supabase.table("performance").insert(new_record).execute()
                st.success("✅ Performance record added successfully!")

    st.markdown("### 📊 Performance History")
    perf_response = supabase.table("performance").select("*").eq("child_id", selected_id).order("term").execute()
    records = perf_response.data or []

    if records:
        df = p


def profile():
    st.markdown("""
        <style>
            .profile-title {
                color: #6a1b9a;
                text-align: center;
                font-size: 2em;
                font-weight: bold;
                margin-bottom: 20px;
            }
            .child-card {
                background-color: #f0f8ff;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .child-field {
                font-weight: 500;
                margin-bottom: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="profile-title">👤 View Child Profile</div>', unsafe_allow_html=True)

    # Fetch group/class options
    groups_response = supabase.table("children").select("group_class").neq("group_class", "").execute()
    groups = sorted({row['group_class'] for row in groups_response.data}) if groups_response.data else []

    if not groups:
        st.warning("⚠️ No groups found. Please register children first.")
        return

    group = st.selectbox("Select Group/Class", groups)
    
    children_response = supabase.table("children").select("id, full_name").eq("group_class", group).execute()
    children_list = children_response.data or []

    if not children_list:
        st.info(f"No children found in group '{group}'.")
        return

    selected_name = st.selectbox("Select Child", [child['full_name'] for child in children_list])

    selected_child = next((child for child in children_list if child['full_name'] == selected_name), None)

    if selected_child:
        child_id = selected_child['id']
        # Fetch full record
        record_response = supabase.table("children").select("*").eq("id", child_id).execute()
        if record_response.data:
            child = record_response.data[0]
            st.markdown(f"""
                <div class="child-card">
                    <div class="child-field"><strong>Full Name:</strong> {child.get('full_name', 'N/A')}</div>
                    <div class="child-field"><strong>Age:</strong> {child.get('age', 'N/A')}</div>
                    <div class="child-field"><strong>Date of Birth:</strong> {child.get('date_of_birth', 'N/A')}</div>
                    <div class="child-field"><strong>Grade:</strong> {child.get('grade', 'N/A')}</div>
                    <div class="child-field"><strong>Location:</strong> {child.get('location', 'N/A')}</div>
                    <div class="child-field"><strong>Group/Class:</strong> {child.get('group_class', 'N/A')}</div>
                    <div class="child-field"><strong>Guardian Name:</strong> {child.get('guardian_name', 'N/A')}</div>
                    <div class="child-field"><strong>Guardian Contact:</strong> {child.get('guardian_contact', 'N/A')}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Child record not found.")


def edit_profile():
    st.markdown("<h2 style='color:#ff69b4;'>✏️ Edit Child Profile</h2>", unsafe_allow_html=True)

    # Fetch groups for filter
    groups_response = supabase.table("children").select("group_class").neq("group_class", "").execute()
    groups = list({row['group_class'] for row in groups_response.data}) if groups_response.data else []
    groups.sort()
    groups.insert(0, "All Groups")

    selected_group = st.selectbox("Filter by Group/Class", groups)

    # Fetch children based on group or all
    if selected_group == "All Groups":
        children_resp = supabase.table("children").select("id, full_name").execute()
    else:
        children_resp = supabase.table("children").select("id, full_name").eq("group_class", selected_group).execute()

    children_list = children_resp.data or []
    if not children_list:
        st.info("No children found for the selected group.")
        return

    child_options = {child['full_name']: child['id'] for child in children_list}
    selected_child_name = st.selectbox("Select Child to Edit", ["-- Select --"] + list(child_options.keys()))

    if selected_child_name == "-- Select --":
        st.info("Please select a child to edit.")
        return

    child_id = child_options[selected_child_name]

    # Fetch current child info
    child_resp = supabase.table("children").select("*").eq("id", child_id).maybe_single().execute()
    child = child_resp.data

    if not child:
        st.error("Child data not found.")
        return

    # Editable form with pre-filled values
    with st.form("edit_profile_form"):
        full_name = st.text_input("Full Name", value=child['full_name'])
        age = st.number_input("Age", min_value=0, max_value=25, value=child['age'])
        birthdate = st.date_input("Birthdate", value=pd.to_datetime(child['birthdate']).date())
        grade = st.text_input("Grade", value=child['grade'])
        location = st.text_input("Location", value=child['location'])
        group_class = st.text_input("Group/Class", value=child['group_class'])
        guardian_name = st.text_input("Guardian Name", value=child['guardian_name'])
        guardian_contact = st.text_input("Guardian Contact", value=child['guardian_contact'])

        submitted = st.form_submit_button("💾 Save Changes")
        delete_button = st.form_submit_button("🗑️ Delete Profile")

        if submitted:
            try:
                update_data = {
                    "full_name": full_name,
                    "age": age,
                    "birthdate": birthdate.isoformat(),
                    "grade": grade,
                    "location": location,
                    "group_class": group_class,
                    "guardian_name": guardian_name,
                    "guardian_contact": guardian_contact
                }
                supabase.table("children").update(update_data).eq("id", child_id).execute()
                st.success("✅ Profile updated successfully!")
            except Exception as e:
                st.error(f"❌ Error updating profile: {e}")
        if delete_button:
            confirm = st.radio("Are you sure you want to delete this profile?", ("No", "Yes"), index=0)
            if confirm == "Yes":
                try:
                    delete_response = supabase.table("children").delete().eq("id", child_id).execute()
                    if delete_response.data is not None:
                        st.success("✅ Profile deleted successfully.")
                        st.stop()
                    else:
                        st.error("❌ Failed to delete profile.")
                except Exception as e:
                    st.error(f"❌ Error deleting profile: {e}")

# Page selector
if page == "Home":
    home()
elif page == "Register Child":
    register_child()
elif page == "Attendance":
    attendance()
elif page == "Reports":
    reports()
elif page == "Performance":
    performance()
elif page == "Profile":
    profile()
elif page == "Edit Profile":
    edit_profile()

