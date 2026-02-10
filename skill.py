#!/usr/bin/env python3
"""
skill.py - Skill training and management CLI tool
Similar to skill.sh for managing agent skills
"""
import sys
import os
import argparse
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.skills import SkillManager


def list_skills(skill_manager):
    """List all available skills."""
    print("=" * 60)
    print("📚 Available Skills")
    print("=" * 60)
    
    skills = skill_manager.list_skills()
    
    if not skills:
        print("No skills available.")
        return
    
    for skill in skills:
        print(f"\n🎯 {skill['name']}")
        print(f"   ID: {skill['skill_id']}")
        print(f"   Description: {skill['description']}")
        print(f"   Level: {skill['level']}/10")
        print(f"   Experience: {skill['experience']} XP")
        print(f"   Usage: {skill['usage_count']} times")
        print(f"   Success Rate: {skill['proficiency']:.1%}")
        if skill['last_used']:
            print(f"   Last Used: {skill['last_used']}")
    
    print("\n" + "=" * 60)


def show_leaderboard(skill_manager):
    """Show skill leaderboard."""
    print("=" * 60)
    print("🏆 Skill Leaderboard")
    print("=" * 60)
    
    leaderboard = skill_manager.get_leaderboard()
    
    if not leaderboard:
        print("No skills to rank.")
        return
    
    for i, skill in enumerate(leaderboard, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        print(f"\n{medal} {skill['name']}")
        print(f"    Level: {skill['level']}/10")
        print(f"    Proficiency: {skill['proficiency']:.1%}")
        print(f"    Usage: {skill['usage_count']} times")
    
    print("\n" + "=" * 60)


def train_skill(skill_manager, skill_id, examples_file):
    """Train a skill with examples from file."""
    print(f"📚 Training skill: {skill_id}")
    
    if not os.path.exists(examples_file):
        print(f"❌ Training file not found: {examples_file}")
        return
    
    # Load training data
    with open(examples_file, 'r') as f:
        training_data = json.load(f)
    
    print(f"📖 Loaded {len(training_data)} training examples")
    
    # Train the skill
    result = skill_manager.train_skill(skill_id, training_data)
    
    if result.get('success'):
        print(f"✅ Training completed!")
        print(f"   Examples trained: {result['examples_trained']}")
        
        # Show updated stats
        stats = skill_manager.get_skill_stats(skill_id)
        if stats:
            print(f"   New level: {stats['level']}/10")
            print(f"   Total experience: {stats['experience']} XP")
    else:
        print(f"❌ Training failed: {result.get('error', 'Unknown error')}")


def test_skill(skill_manager, skill_id, test_file):
    """Test a skill with test data."""
    print(f"🧪 Testing skill: {skill_id}")
    
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return
    
    # Load test data
    with open(test_file, 'r') as f:
        test_data = json.load(f)
    
    print(f"📖 Loaded {len(test_data)} test cases")
    
    success_count = 0
    for i, test_case in enumerate(test_data, 1):
        context = test_case.get('context', {})
        expected = test_case.get('expected', {})
        
        result = skill_manager.execute_skill(skill_id, context)
        
        if result.get('success'):
            success_count += 1
            print(f"   ✅ Test {i}: PASS")
        else:
            print(f"   ❌ Test {i}: FAIL - {result.get('error', 'Unknown error')}")
    
    print(f"\n📊 Results: {success_count}/{len(test_data)} tests passed ({success_count/len(test_data):.1%})")


def reset_skill(skill_manager, skill_id):
    """Reset a skill to initial state."""
    print(f"🔄 Resetting skill: {skill_id}")
    
    if skill_manager.reset_skill(skill_id):
        print(f"✅ Skill reset successfully")
    else:
        print(f"❌ Failed to reset skill")


def export_report(skill_manager, output_file):
    """Export skills report."""
    print(f"📄 Exporting skills report to: {output_file}")
    
    skill_manager.export_skills_report(output_file)
    
    print(f"✅ Report exported successfully")


def create_training_template(output_file):
    """Create a training data template."""
    template = [
        {
            "context": {
                "email_text": "Sample email text here",
                "subject": "Sample subject",
                "body": "Sample body"
            },
            "expected": {
                "email": ["example@email.com"],
                "category": "general"
            }
        }
    ]
    
    with open(output_file, 'w') as f:
        json.dump(template, f, indent=2)
    
    print(f"✅ Training template created: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Skill training and management tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all skills
  python skill.py list
  
  # Show leaderboard
  python skill.py leaderboard
  
  # Train a skill
  python skill.py train email_parsing training_data.json
  
  # Test a skill
  python skill.py test email_classification test_data.json
  
  # Reset a skill
  python skill.py reset email_parsing
  
  # Export report
  python skill.py export skills_report.json
  
  # Create training template
  python skill.py template training_template.json
        """
    )
    
    parser.add_argument('command', choices=[
        'list', 'leaderboard', 'train', 'test', 'reset', 'export', 'template'
    ], help='Command to execute')
    
    parser.add_argument('args', nargs='*', help='Command arguments')
    
    args = parser.parse_args()
    
    # Initialize skill manager
    skill_manager = SkillManager()
    
    # Execute command
    if args.command == 'list':
        list_skills(skill_manager)
    
    elif args.command == 'leaderboard':
        show_leaderboard(skill_manager)
    
    elif args.command == 'train':
        if len(args.args) < 2:
            print("❌ Usage: skill.py train <skill_id> <training_file.json>")
            sys.exit(1)
        train_skill(skill_manager, args.args[0], args.args[1])
    
    elif args.command == 'test':
        if len(args.args) < 2:
            print("❌ Usage: skill.py test <skill_id> <test_file.json>")
            sys.exit(1)
        test_skill(skill_manager, args.args[0], args.args[1])
    
    elif args.command == 'reset':
        if len(args.args) < 1:
            print("❌ Usage: skill.py reset <skill_id>")
            sys.exit(1)
        reset_skill(skill_manager, args.args[0])
    
    elif args.command == 'export':
        output_file = args.args[0] if args.args else 'skills_report.json'
        export_report(skill_manager, output_file)
    
    elif args.command == 'template':
        output_file = args.args[0] if args.args else 'training_template.json'
        create_training_template(output_file)


if __name__ == "__main__":
    main()
