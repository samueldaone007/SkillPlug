from django.db import migrations
 
SKILLS = [
    # Tech & Design
    "Web Development",
    "Mobile App Development",
    "UI/UX Design",
    "Graphic Design",
    "Logo & Branding Design",
    "Video Editing",
    "Photo Editing",
    "Motion Graphics",
    "3D Modelling",
    # Writing & Media
    "Academic Writing",
    "Copywriting & Content",
    "Proofreading & Editing",
    "Social Media Management",
    "Photography",
    "Voiceover & Narration",
    # Business & Admin
    "Data Entry",
    "Virtual Assistant",
    "Customer Support",
    "Accounting & Bookkeeping",
    "Research & Analysis",
    # Trades & Lifestyle
    "Hairdressing & Styling",
    "Nail Technology",
    "Makeup Artistry",
    "Fashion & Tailoring",
    "Catering & Baking",
    "Event Planning",
    "Cleaning Services",
    "Laundry & Ironing",
    # Tutoring & Training
    "Tutoring & Teaching",
    "Music Lessons",
    "Fitness & Personal Training",
    "Language Translation",
]
 
 
def seed_skills(apps, schema_editor):
    Skill = apps.get_model('accounts', 'Skill')
    for name in SKILLS:
        Skill.objects.get_or_create(name=name)
 
 
def unseed_skills(apps, schema_editor):
    Skill = apps.get_model('accounts', 'Skill')
    Skill.objects.filter(name__in=SKILLS).delete()
 
 
class Migration(migrations.Migration):
 
    dependencies = [
        ('accounts', '0001_initial'),
    ]
 
    operations = [
        migrations.RunPython(seed_skills, unseed_skills),
    ]