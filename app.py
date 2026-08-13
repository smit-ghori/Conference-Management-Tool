import os
import csv
import io
import random
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cmt-ljku-codeapex-ieee-secret-key-2026-auth'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

db = SQLAlchemy(app)

# Ensure upload directories exist
for folder in ['brochures', 'flyers', 'papers']:
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], folder), exist_ok=True)


# --- Database Models ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='author')  # 'admin' or 'author'
    institution = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship('Submission', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50), nullable=False, default='laptop-code')


class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    acronym = db.Column(db.String(50), nullable=False)
    department_code = db.Column(db.String(20), db.ForeignKey('department.code'), nullable=False)
    state = db.Column(db.String(20), nullable=False, default='upcoming')  # 'current', 'upcoming', 'past'
    start_date = db.Column(db.String(50), nullable=False)
    end_date = db.Column(db.String(50), nullable=False)
    submission_deadline = db.Column(db.String(50), nullable=True)
    venue = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    call_for_papers = db.Column(db.Text, nullable=True)
    registration_fee = db.Column(db.Float, nullable=False, default=1000.0)
    brochure_filename = db.Column(db.String(200), nullable=True)
    flyer_filename = db.Column(db.String(200), nullable=True)
    report_summary = db.Column(db.Text, nullable=True)
    key_speakers = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    department = db.relationship('Department', backref=db.backref('conferences', lazy=True))
    schedules = db.relationship('ScheduleItem', backref='conference', cascade='all, delete-orphan', lazy=True)
    updates = db.relationship('LiveUpdate', backref='conference', cascade='all, delete-orphan', lazy=True)
    submissions = db.relationship('Submission', backref='conference', cascade='all, delete-orphan', lazy=True)


class ScheduleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'), nullable=False)
    day_label = db.Column(db.String(50), nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)
    session_title = db.Column(db.String(200), nullable=False)
    speaker = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=False)


class LiveUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'), nullable=False)
    timestamp_str = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    badge_type = db.Column(db.String(20), default='info')


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    abstract_id = db.Column(db.String(30), unique=True, nullable=False)
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    author_name = db.Column(db.String(100), nullable=False)
    author_email = db.Column(db.String(120), nullable=False)
    author_phone = db.Column(db.String(20), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    department_code = db.Column(db.String(20), nullable=False)
    presentation_type = db.Column(db.String(30), nullable=False)  # 'Paper Presentation' or 'Poster Presentation'
    paper_title = db.Column(db.String(250), nullable=False)
    abstract_text = db.Column(db.Text, nullable=False)
    paper_filename = db.Column(db.String(200), nullable=True)
    payment_status = db.Column(db.String(20), default='Pending')
    payment_ref = db.Column(db.String(100), nullable=True)
    verification_status = db.Column(db.String(30), default='Under Review')
    registration_fee = db.Column(db.Float, nullable=False, default=1000.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Helper function to generate unique Abstract ID
def generate_abstract_id(dept_code):
    year = datetime.now().year
    rand_num = random.randint(1000, 9999)
    abstract_id = f"CMT-{year}-{dept_code}-{rand_num}"
    while Submission.query.filter_by(abstract_id=abstract_id).first():
        rand_num = random.randint(1000, 9999)
        abstract_id = f"CMT-{year}-{dept_code}-{rand_num}"
    return abstract_id


# --- Auth Decorators ---

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_role') != 'admin':
            flash("Access denied. Administrator privileges required.", "danger")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# --- Context Processor for Global Template Data ---

@app.context_processor
def inject_global_data():
    departments = Department.query.order_by(Department.name).all()
    current_user = None
    if 'user_id' in session:
        current_user = User.query.get(session['user_id'])
    return dict(
        departments=departments,
        current_user=current_user,
        current_year=datetime.now().year
    )


# --- Authentication Routes ---

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        institution = request.form.get('institution')
        phone = request.form.get('phone')

        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists. Please login.", "warning")
            return redirect(url_for('signup'))

        new_user = User(
            name=name,
            email=email,
            institution=institution,
            phone=phone,
            role='author'
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Automatically log in new user
        session['user_id'] = new_user.id
        session['user_name'] = new_user.name
        session['user_role'] = new_user.role

        flash("Account created successfully! Welcome to the CMT Portal.", "success")
        return redirect(url_for('home'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role

            flash(f"Welcome back, {user.name}!", "success")
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            if user.role == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('my_submissions'))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))


@app.route('/my-submissions')
@login_required
def my_submissions():
    user = User.query.get_or_404(session['user_id'])
    # Query user submissions linked by user_id OR email
    submissions = Submission.query.filter(
        (Submission.user_id == user.id) | (Submission.author_email.ilike(user.email))
    ).order_by(Submission.id.desc()).all()

    return render_template('my_submissions.html', user=user, submissions=submissions)


# --- Core Public Routes ---

@app.route('/')
def home():
    selected_dept = request.args.get('dept', '')
    query = Conference.query.filter_by(state='current')
    if selected_dept:
        query = query.filter_by(department_code=selected_dept)
    
    current_conferences = query.all()
    upcoming_count = Conference.query.filter_by(state='upcoming').count()
    past_count = Conference.query.filter_by(state='past').count()
    current_count = Conference.query.filter_by(state='current').count()

    return render_template(
        'home.html',
        current_conferences=current_conferences,
        selected_dept=selected_dept,
        current_count=current_count,
        upcoming_count=upcoming_count,
        past_count=past_count
    )


@app.route('/upcoming')
def upcoming():
    selected_dept = request.args.get('dept', '')
    query = Conference.query.filter_by(state='upcoming')
    if selected_dept:
        query = query.filter_by(department_code=selected_dept)
    
    upcoming_conferences = query.order_by(Conference.id.desc()).all()
    return render_template(
        'upcoming.html',
        upcoming_conferences=upcoming_conferences,
        selected_dept=selected_dept
    )


@app.route('/archive')
def archive():
    selected_dept = request.args.get('dept', '')
    query = Conference.query.filter_by(state='past')
    if selected_dept:
        query = query.filter_by(department_code=selected_dept)
    
    past_conferences = query.order_by(Conference.id.desc()).all()
    return render_template(
        'archive.html',
        past_conferences=past_conferences,
        selected_dept=selected_dept
    )


@app.route('/conference/<int:conf_id>')
def conference_detail(conf_id):
    conf = Conference.query.get_or_404(conf_id)
    return render_template('conference_detail.html', conference=conf)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        conf_id = request.form.get('conference_id')
        author_name = request.form.get('author_name')
        author_email = request.form.get('author_email')
        author_phone = request.form.get('author_phone')
        institution = request.form.get('institution')
        presentation_type = request.form.get('presentation_type')
        paper_title = request.form.get('paper_title')
        abstract_text = request.form.get('abstract_text')

        conf = Conference.query.get_or_404(conf_id)

        file = request.files.get('paper_file')
        paper_filename = None
        if file and file.filename:
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'papers', filename)
            file.save(save_path)
            paper_filename = filename

        abstract_id = generate_abstract_id(conf.department_code)

        # Associate with current user if logged in
        user_id = session.get('user_id')

        new_sub = Submission(
            abstract_id=abstract_id,
            conference_id=conf.id,
            user_id=user_id,
            author_name=author_name,
            author_email=author_email,
            author_phone=author_phone,
            institution=institution,
            department_code=conf.department_code,
            presentation_type=presentation_type,
            paper_title=paper_title,
            abstract_text=abstract_text,
            paper_filename=paper_filename,
            registration_fee=conf.registration_fee,
            payment_status='Pending',
            verification_status='Under Review'
        )

        db.session.add(new_sub)
        db.session.commit()

        flash(f"Submission successful! Your unique Abstract ID is {abstract_id}.", "success")
        return redirect(url_for('payment', sub_id=new_sub.id))

    preselect_conf_id = request.args.get('conf_id', type=int)
    open_conferences = Conference.query.filter(Conference.state.in_(['current', 'upcoming'])).all()
    return render_template('submit.html', open_conferences=open_conferences, preselect_conf_id=preselect_conf_id)


@app.route('/lookup', methods=['GET', 'POST'])
def lookup():
    submission = None
    query_str = ""
    if request.method == 'POST':
        query_str = request.form.get('query_str', '').strip()
        if query_str:
            submission = Submission.query.filter(
                (Submission.abstract_id.ilike(query_str)) | (Submission.author_email.ilike(query_str))
            ).first()
            if not submission:
                flash(f"No submission found for '{query_str}'. Please check your Abstract ID or Email.", "warning")

    return render_template('lookup.html', submission=submission, query_str=query_str)


@app.route('/payment/<int:sub_id>', methods=['GET', 'POST'])
def payment(sub_id):
    submission = Submission.query.get_or_404(sub_id)

    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        tx_ref = f"PAY-{random.randint(10000000, 99999999)}"
        submission.payment_status = 'Paid'
        submission.payment_ref = f"{payment_method.upper()}-{tx_ref}"
        if submission.verification_status == 'Under Review':
            submission.verification_status = 'Verified'
        
        db.session.commit()
        flash("Payment completed successfully! Official receipt generated.", "success")
        return redirect(url_for('receipt', sub_id=submission.id))

    return render_template('payment.html', submission=submission)


@app.route('/receipt/<int:sub_id>')
def receipt(sub_id):
    submission = Submission.query.get_or_404(sub_id)
    return render_template('receipt.html', submission=submission)


# --- Protected Admin Portal & Advanced Management Routes ---

@app.route('/admin', methods=['GET', 'POST'])
@admin_required
def admin():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_conference':
            title = request.form.get('title')
            acronym = request.form.get('acronym')
            dept_code = request.form.get('department_code')
            state = request.form.get('state')
            
            def format_date_str(raw_date):
                if not raw_date:
                    return ""
                try:
                    dt = datetime.strptime(raw_date, '%Y-%m-%d')
                    return dt.strftime('%B %d, %Y')
                except ValueError:
                    return raw_date

            start_date = format_date_str(request.form.get('start_date'))
            end_date = format_date_str(request.form.get('end_date'))
            deadline = format_date_str(request.form.get('submission_deadline'))
            venue = request.form.get('venue')
            fee = float(request.form.get('registration_fee', 1000))
            description = request.form.get('description')
            cfp = request.form.get('call_for_papers')
            speakers = request.form.get('key_speakers')

            new_conf = Conference(
                title=title,
                acronym=acronym,
                department_code=dept_code,
                state=state,
                start_date=start_date,
                end_date=end_date,
                submission_deadline=deadline,
                venue=venue,
                registration_fee=fee,
                description=description,
                call_for_papers=cfp,
                key_speakers=speakers,
                brochure_filename='sample_brochure.pdf',
                flyer_filename='sample_flyer.pdf'
            )
            db.session.add(new_conf)
            db.session.commit()
            flash(f"Conference '{title}' added successfully!", "success")
            return redirect(url_for('admin'))

        elif action == 'update_submission_status':
            sub_id = request.form.get('submission_id')
            v_status = request.form.get('verification_status')
            p_status = request.form.get('payment_status')
            
            sub = Submission.query.get(sub_id)
            if sub:
                sub.verification_status = v_status
                sub.payment_status = p_status
                db.session.commit()
                flash(f"Submission {sub.abstract_id} updated successfully.", "success")
            return redirect(url_for('admin'))

        elif action == 'change_conf_state':
            conf_id = request.form.get('conf_id')
            new_state = request.form.get('new_state')
            conf = Conference.query.get(conf_id)
            if conf:
                conf.state = new_state
                db.session.commit()
                flash(f"State for conference '{conf.acronym}' changed to {new_state.capitalize()}.", "info")
            return redirect(url_for('admin'))

    # Query params for initial values if passed in URL
    search_q = request.args.get('q', '').strip()
    status_filter = request.args.get('status', '')
    dept_filter = request.args.get('dept', '')
    type_filter = request.args.get('type', '')
    conf_q = request.args.get('conf_q', '').strip()
    conf_state_filter = request.args.get('conf_state', '')
    conf_dept_filter = request.args.get('conf_dept', '')

    # Fetch all submissions and conferences so DOM has full dataset for instant zero-reload live filtering
    submissions = Submission.query.order_by(Submission.id.desc()).all()
    all_conferences = Conference.query.order_by(Conference.id.desc()).all()

    total_submissions = Submission.query.count()
    verified_count = Submission.query.filter_by(verification_status='Verified').count()
    accepted_count = Submission.query.filter_by(verification_status='Accepted').count()
    paid_submissions = Submission.query.filter_by(payment_status='Paid').all()
    total_revenue = sum([s.registration_fee for s in paid_submissions])
    paper_count = Submission.query.filter_by(presentation_type='Paper Presentation').count()
    poster_count = Submission.query.filter_by(presentation_type='Poster Presentation').count()

    return render_template(
        'admin.html',
        submissions=submissions,
        conferences=all_conferences,
        search_q=search_q,
        status_filter=status_filter,
        dept_filter=dept_filter,
        type_filter=type_filter,
        conf_q=conf_q,
        conf_state_filter=conf_state_filter,
        conf_dept_filter=conf_dept_filter,
        total_submissions=total_submissions,
        verified_count=verified_count,
        accepted_count=accepted_count,
        total_revenue=total_revenue,
        paper_count=paper_count,
        poster_count=poster_count
    )


@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    admin_user = User.query.get_or_404(session['user_id'])
    
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_email = request.form.get('email', '').strip().lower()
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Verify current password
        if not admin_user.check_password(current_password):
            flash("Current password is incorrect. Unable to update profile.", "danger")
            return redirect(url_for('admin_settings'))

        # Check email uniqueness if changing email
        if new_email != admin_user.email and User.query.filter_by(email=new_email).first():
            flash("That email is already in use by another user account.", "danger")
            return redirect(url_for('admin_settings'))

        admin_user.name = new_name
        admin_user.email = new_email

        # If updating password
        if new_password:
            if new_password != confirm_password:
                flash("New passwords do not match. Please re-enter.", "danger")
                return redirect(url_for('admin_settings'))
            admin_user.set_password(new_password)
            flash("Admin ID (email) and Password updated successfully!", "success")
        else:
            flash("Admin details updated successfully!", "success")

        db.session.commit()
        session['user_name'] = admin_user.name
        return redirect(url_for('admin_settings'))

    return render_template('admin_settings.html', admin_user=admin_user)


@app.route('/admin/delete-submission/<int:sub_id>', methods=['POST'])
@admin_required
def delete_submission(sub_id):
    sub = Submission.query.get_or_404(sub_id)
    abstract_id = sub.abstract_id
    db.session.delete(sub)
    db.session.commit()
    flash(f"Submission {abstract_id} deleted permanently.", "info")
    return redirect(url_for('admin'))


@app.route('/admin/export-csv')
@admin_required
def export_csv():
    submissions = Submission.query.order_by(Submission.id.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        'Abstract ID', 'Conference', 'Author Name', 'Author Email', 'Phone',
        'Institution', 'Department', 'Presentation Type', 'Paper Title',
        'Verification Status', 'Payment Status', 'Registration Fee', 'Payment Ref', 'Submitted At'
    ])

    for s in submissions:
        conf_title = s.conference.acronym if s.conference else 'N/A'
        writer.writerow([
            s.abstract_id, conf_title, s.author_name, s.author_email, s.author_phone,
            s.institution, s.department_code, s.presentation_type, s.paper_title,
            s.verification_status, s.payment_status, s.registration_fee, s.payment_ref or 'N/A',
            s.created_at.strftime('%Y-%m-%d %H:%M')
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=cmt_submissions_report.csv"}
    )


@app.route('/download/<file_type>/<filename>')
def download_file(file_type, filename):
    if file_type not in ['brochures', 'flyers', 'papers']:
        flash("Invalid file category.", "danger")
        return redirect(url_for('home'))
    
    dir_path = os.path.join(app.config['UPLOAD_FOLDER'], file_type)
    file_full_path = os.path.join(dir_path, filename)

    if not os.path.exists(file_full_path):
        with open(file_full_path, 'w', encoding='utf-8') as f:
            f.write(f"--- LJKU Conference Management Tool (CMT) Document ---\n"
                    f"Category: {file_type.capitalize()}\n"
                    f"File Name: {filename}\n"
                    f"Organized by: IEEE Student Branch, LJ University & CODEAPEX\n"
                    f"Date: 8th August 2026\n"
                    f"Description: Official conference material for participant reference.\n")

    return send_from_directory(dir_path, filename, as_attachment=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
