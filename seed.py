import os
from app import app, db, User, Department, Conference, ScheduleItem, LiveUpdate, Submission

def seed_database():
    with app.app_context():
        # Re-create database schema
        db.drop_all()
        db.create_all()

        print("Seeding Users (Admin & Authors)...")
        # 1. Admin User
        admin_user = User(
            name="System Administrator",
            email="admin@ljku.edu.in",
            role="admin",
            institution="LJKU Central Administration",
            phone="+91 9998887770"
        )
        admin_user.set_password("admin123")

        # 2. Author User
        author_user = User(
            name="Aarav Sharma",
            email="aarav.sharma@example.edu",
            role="author",
            institution="LJ University - Department of Computer Science",
            phone="+91 9876543210"
        )
        author_user.set_password("user123")

        db.session.add_all([admin_user, author_user])
        db.session.commit()

        print("Seeding Departments...")
        departments = [
            Department(code='CSE', name='Computer Science & Engineering', icon='fa-laptop-code'),
            Department(code='ECE', name='Electronics & Communication Engineering', icon='fa-microchip'),
            Department(code='MECH', name='Mechanical Engineering', icon='fa-cogs'),
            Department(code='CIVIL', name='Civil Engineering', icon='fa-building'),
            Department(code='IT', name='Information Technology', icon='fa-network-wired'),
            Department(code='AIDS', name='Artificial Intelligence & Data Science', icon='fa-brain')
        ]
        db.session.add_all(departments)
        db.session.commit()

        print("Seeding Conferences...")
        # 1. Current Conferences
        conf_current_1 = Conference(
            title="IEEE International Conference on Next-Gen Computing & AI Systems",
            acronym="ICNC-2026",
            department_code="CSE",
            state="current",
            start_date="August 13, 2026",
            end_date="August 15, 2026",
            submission_deadline="July 25, 2026",
            venue="Main University Auditorium, LJKU Campus",
            registration_fee=1500.0,
            description="A flagship international gathering showcasing state-of-the-art breakthroughs in artificial intelligence, distributed systems, high-performance computing, and quantum algorithms.",
            call_for_papers="We invite full-length research papers and technical posters on tracks including: Deep Learning Models, Edge AI, Distributed Consensus Systems, Cloud Native Architectures, and Cyber-Physical Systems.",
            key_speakers="Dr. Rajesh Patel (Director, AI Research Lab) | Prof. Elena Rostova (MIT) | Er. Vikram Mehta (Chief Architect, TechCorp)",
            brochure_filename="icnc2026_brochure.pdf",
            flyer_filename="icnc2026_flyer.pdf",
            report_summary="Ongoing technical event organized jointly by IEEE Student Branch LJKU and CODEAPEX."
        )

        conf_current_2 = Conference(
            title="IEEE Conference on Smart Sensor Networks & Industrial Robotics",
            acronym="IC-ROBOTICS 2026",
            department_code="ECE",
            state="current",
            start_date="August 12, 2026",
            end_date="August 14, 2026",
            submission_deadline="July 20, 2026",
            venue="ECE Department Seminar Hall 3, LJKU",
            registration_fee=1800.0,
            description="Exemplifying modern sensor fusion, IoT communication protocols, micro-electromechanical systems (MEMS), and industrial automation.",
            call_for_papers="Submissions invited for hardware prototypes, poster presentations, and theoretical research on RF communication, embedded systems, and autonomous robotics.",
            key_speakers="Dr. S. K. Nambiar (ISRO Fellow) | Prof. Hannah Vance (Cambridge Microelectronics)",
            brochure_filename="microbots_brochure.pdf",
            flyer_filename="microbots_flyer.pdf",
            report_summary="Live conference currently hosting 180+ delegates."
        )

        # 2. Upcoming Conferences
        conf_upcoming_1 = Conference(
            title="National Conference on Sustainable Materials & Green Infrastructure",
            acronym="IC-GREEN 2026",
            department_code="CIVIL",
            state="upcoming",
            start_date="September 20, 2026",
            end_date="September 22, 2026",
            submission_deadline="September 05, 2026",
            venue="Civil Block Convention Center, LJKU",
            registration_fee=1200.0,
            description="Focusing on zero-carbon concrete formulations, resilient structural engineering, urban hydrology, and eco-friendly construction technologies.",
            call_for_papers="Original papers invited in tracks: Sustainable Concrete Technology, Smart Transportation Networks, Environmental Impact Assessment, and Earthquake Engineering.",
            key_speakers="Dr. Ananya Roy (National Institute of Urban Affairs) | Er. Suresh Dave (L&T Infrastructure)",
            brochure_filename="green_brochure.pdf",
            flyer_filename="green_flyer.pdf"
        )

        conf_upcoming_2 = Conference(
            title="International Summit on Automotive Engineering & Thermal Dynamics",
            acronym="IC-AUTOTECH 2026",
            department_code="MECH",
            state="upcoming",
            start_date="October 10, 2026",
            end_date="October 12, 2026",
            submission_deadline="September 25, 2026",
            venue="Mechanical Engineering Workshop & Auditorium, LJKU",
            registration_fee=1500.0,
            description="A global convention highlighting electric vehicle (EV) powertrains, computational fluid dynamics (CFD), battery management systems, and additive manufacturing.",
            call_for_papers="Call for papers and poster presentations in EV Battery Cooling, Aerodynamic Modeling, Advanced CAD/CAM, and Renewable Thermal Energy Systems.",
            key_speakers="Dr. Martin Vance (EV Propulsion Systems) | Prof. Devang Joshi (IIT Bombay)",
            brochure_filename="autotech_brochure.pdf",
            flyer_filename="autotech_flyer.pdf"
        )

        conf_upcoming_3 = Conference(
            title="IEEE Symposium on Cloud Security, DevOps & Microservices",
            acronym="IC-CLOUDSYS 2026",
            department_code="IT",
            state="upcoming",
            start_date="November 05, 2026",
            end_date="November 07, 2026",
            submission_deadline="October 15, 2026",
            venue="IT Block Cyber Lab 1, LJKU",
            registration_fee=1400.0,
            description="Exploring zero-trust network architectures, serverless computing performance, Kubernetes container orchestration security, and infrastructure as code.",
            call_for_papers="Submissions invited for technical papers and industry case studies on DevSecOps, Service Meshes, Continuous Delivery, and Cloud Threat Modeling.",
            key_speakers="Ms. Priya Sharma (Cloud Architect, AWS) | Mr. Rahul Verma (DevOps Practice Lead)",
            brochure_filename="cloudsys_brochure.pdf",
            flyer_filename="cloudsys_flyer.pdf"
        )

        conf_upcoming_4 = Conference(
            title="Global Congress on Machine Learning & Knowledge Discovery",
            acronym="IC-DATAMIND 2026",
            department_code="AIDS",
            state="upcoming",
            start_date="December 01, 2026",
            end_date="December 03, 2026",
            submission_deadline="November 10, 2026",
            venue="CODEAPEX Center of Excellence, LJKU",
            registration_fee=2000.0,
            description="Advancing frontier research in Large Language Models (LLMs), Computer Vision, Responsible AI, and Knowledge Graphs for health informatics.",
            call_for_papers="Accepting research papers and interactive poster presentations across multimodal AI, neural architecture search, explainable AI, and Big Data pipelines.",
            key_speakers="Dr. Geoffrey Miller (Stanford AI Lab) | Dr. Neha Agarwal (Google DeepMind)",
            brochure_filename="datamind_brochure.pdf",
            flyer_filename="datamind_flyer.pdf"
        )

        # 3. Past Conferences
        conf_past_1 = Conference(
            title="International Symposium on Cyber Security & Blockchain Infrastructure",
            acronym="IC-CYBERSEC 2025",
            department_code="CSE",
            state="past",
            start_date="November 18, 2025",
            end_date="November 20, 2025",
            venue="Main Auditorium, LJKU Campus",
            registration_fee=1500.0,
            description="Successfully completed conference covering cryptography, smart contract audits, and threat telemetry.",
            call_for_papers="Archived call for papers. 120 submissions received.",
            report_summary="Outcome Report: The conference attracted 340 delegates from 14 countries. 85 full papers were selected and published in IEEE Xplore Digital Library. Best Paper Award went to 'Post-Quantum Lattice Cryptography in IoT Networks'.",
            brochure_filename="cybersec2025_brochure.pdf",
            flyer_filename="cybersec2025_flyer.pdf"
        )

        conf_past_2 = Conference(
            title="National Conference on Semiconductor Physics & VLSI Design",
            acronym="IC-VLSI 2025",
            department_code="ECE",
            state="past",
            start_date="September 10, 2025",
            end_date="September 12, 2025",
            venue="ECE Auditorium, LJKU",
            registration_fee=1200.0,
            description="Archived event on 3nm lithography, FinFET technology, and low-power ASIC design.",
            call_for_papers="Archived call for papers. 95 submissions received.",
            report_summary="Outcome Report: Hosted 210 attendees with 45 technical paper presentations and 20 poster sessions. Key industry partners included Texas Instruments and Synopsys.",
            brochure_filename="vlsi2025_brochure.pdf",
            flyer_filename="vlsi2025_flyer.pdf"
        )

        db.session.add_all([
            conf_current_1, conf_current_2,
            conf_upcoming_1, conf_upcoming_2, conf_upcoming_3, conf_upcoming_4,
            conf_past_1, conf_past_2
        ])
        db.session.commit()

        print("Seeding Live Schedules & Updates for Current Conferences...")
        schedules_icnc = [
            ScheduleItem(conference_id=conf_current_1.id, day_label="Day 1 - Aug 13", time_slot="09:30 AM - 10:30 AM", session_title="Inaugural Keynote & Lighting of the Lamp", speaker="Prof. Vice Chancellor, LJKU", location="Main Auditorium"),
            ScheduleItem(conference_id=conf_current_1.id, day_label="Day 1 - Aug 13", time_slot="10:45 AM - 12:30 PM", session_title="Track 1: Deep Learning Architectures & Transformer Models", speaker="Dr. Rajesh Patel", location="Hall A"),
            ScheduleItem(conference_id=conf_current_1.id, day_label="Day 1 - Aug 13", time_slot="01:30 PM - 03:30 PM", session_title="Track 2: Paper Presentations & Poster Evaluations", speaker="Session Chair: Dr. B. K. Joshi", location="Hall B & Exhibition Foyer"),
            ScheduleItem(conference_id=conf_current_1.id, day_label="Day 2 - Aug 14", time_slot="10:00 AM - 11:30 AM", session_title="Keynote: Quantum Computing Algorithms in 2026", speaker="Prof. Elena Rostova (MIT)", location="Main Auditorium"),
            ScheduleItem(conference_id=conf_current_1.id, day_label="Day 2 - Aug 14", time_slot="02:00 PM - 04:30 PM", session_title="CODEAPEX Hackathon Showcase & Project Demonstrations", speaker="IEEE Student Team", location="Lab Complex 4")
        ]

        updates_icnc = [
            LiveUpdate(conference_id=conf_current_1.id, timestamp_str="Today, 02:15 PM", title="Track 2 Session Chair Update", message="Session Track 2 Paper Presentations in Hall B shifted to 02:00 PM. All authors please arrive 15 minutes prior.", badge_type="urgent"),
            LiveUpdate(conference_id=conf_current_1.id, timestamp_str="Today, 11:45 AM", title="Poster Presentation Foyer Open", message="Poster display stands in Foyer Area A are now active for judge evaluations.", badge_type="info"),
            LiveUpdate(conference_id=conf_current_1.id, timestamp_str="Today, 09:00 AM", title="Registration Desk Open", message="Delegates can collect their physical badge kits and IEEE conference certificates from Desk 1.", badge_type="schedule")
        ]

        db.session.add_all(schedules_icnc + updates_icnc)
        db.session.commit()

        print("Seeding Sample Submissions...")
        submissions = [
            Submission(
                abstract_id="CMT-2026-CSE-1001",
                conference_id=conf_current_1.id,
                user_id=author_user.id,
                author_name="Aarav Sharma",
                author_email="aarav.sharma@example.edu",
                author_phone="+91 9876543210",
                institution="LJ University - Department of Computer Science",
                department_code="CSE",
                presentation_type="Paper Presentation",
                paper_title="Optimized Attention Mechanisms for Real-Time Edge Processing",
                abstract_text="This paper proposes a novel lightweight attention head pruning method that reduces inference latency by 34% on mobile devices while maintaining 98.2% top-1 accuracy.",
                paper_filename="paper_aarav_sharma.pdf",
                payment_status="Paid",
                payment_ref="UPI-98241049281",
                verification_status="Accepted",
                registration_fee=1500.0
            ),
            Submission(
                abstract_id="CMT-2026-CSE-1002",
                conference_id=conf_current_1.id,
                author_name="Riya Trivedi",
                author_email="riya.trivedi@example.org",
                author_phone="+91 9812345678",
                institution="Institute of Technology, Nirma University",
                department_code="CSE",
                presentation_type="Poster Presentation",
                paper_title="Visualizing High-Dimensional Data Pipelines using WebGL",
                abstract_text="An interactive visual analytics poster demonstrating real-time GPU-accelerated embedding projection for telemetry logs.",
                paper_filename="poster_riya_trivedi.pdf",
                payment_status="Paid",
                payment_ref="CARD-7740192830",
                verification_status="Verified",
                registration_fee=1500.0
            ),
            Submission(
                abstract_id="CMT-2026-ECE-2001",
                conference_id=conf_current_2.id,
                author_name="Kabir Merchant",
                author_email="kabir.m@example.com",
                author_phone="+91 9723456789",
                institution="IIT Gandhinagar",
                department_code="ECE",
                presentation_type="Paper Presentation",
                paper_title="Low-Power MEMS Accelerometer for Wearable Health Telemetry",
                abstract_text="We demonstrate a sub-milliwatt micro-sensor system integrated with Bluetooth Low Energy (BLE 5.3) for cardiovascular monitoring.",
                paper_filename="mems_sensor_paper.pdf",
                payment_status="Pending",
                verification_status="Under Review",
                registration_fee=1800.0
            ),
            Submission(
                abstract_id="CMT-2026-CIVIL-3001",
                conference_id=conf_upcoming_1.id,
                author_name="Kavya Joshi",
                author_email="kavya.civil@example.ac.in",
                author_phone="+91 9909876543",
                institution="LJKU Faculty of Engineering",
                department_code="CIVIL",
                presentation_type="Paper Presentation",
                paper_title="Geopolymer Concrete Formulations Using Recycled Fly Ash and Slag",
                abstract_text="Comprehensive mechanical testing of zero-cement concrete achieving 45 MPa compressive strength at 28 days.",
                paper_filename="geopolymer_concrete.pdf",
                payment_status="Paid",
                payment_ref="NETBANK-8823104",
                verification_status="Accepted",
                registration_fee=1200.0
            )
        ]

        db.session.add_all(submissions)
        db.session.commit()

        print("Database Seeding Completed Successfully!")
        print("Admin User Credentials: admin@ljku.edu.in / admin123")
        print("Author User Credentials: aarav.sharma@example.edu / user123")

if __name__ == '__main__':
    seed_database()
