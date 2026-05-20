import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillplug.settings')
django.setup()
from django.contrib.auth import get_user_model
from apps.accounts.models import Skill, Profile

User = get_user_model()

skills_data = ['Web Development', 'Graphic Design', 'Data Entry', 'Academic Writing', 'Social Media Mgmt', 'Video Editing', 'UI/UX Design']
created_skills = [Skill.objects.get_or_create(name=s)[0] for s in skills_data]

schools = ['unilag', 'uniben', 'oau', 'ui', 'futa']
students = [
    {'u': 'tunde_dev', 'n': 'Tunde Adeyemi', 's': 'unilag', 'd': 'Computer Science', 'w': '2348012345678', 'b': 'Full-stack dev specializing in Django & React.'},
    {'u': 'amara_design', 'n': 'Amara Nwosu', 's': 'uniben', 'd': 'Fine Arts', 'w': '2348098765432', 'b': 'Creative UI/UX designer and graphic artist.'},
    {'u': 'chioma_writer', 'n': 'Chioma Obi', 's': 'oau', 'd': 'English', 'w': '2348055555555', 'b': 'Professional academic writer and editor.'},
]

for s in students:
    if not User.objects.filter(username=s['u']).exists():
        u = User.objects.create_user(username=s['u'], password='password123', email=f"{s['u']}@test.com", full_name=s['n'], school=s['s'], department=s['d'], whatsapp=s['w'], bio=s['b'], verified=True, availability_status='available')
        p, _ = Profile.objects.get_or_create(user=u)
        p.skills.set(created_skills[:2])
        print(f"Created student: {s['n']}")

print("Seed data loaded successfully!")