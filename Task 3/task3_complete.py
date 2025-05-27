import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_user_input():
    """Get role/position details from user"""
    print("INTERACTIVE INTERVIEW QUESTION GENERATOR")
    print("=" * 60)
    print("Enter details about the role you want to generate interview questions for:\n")
    
    role = input("Job Title/Role (e.g., 'Software Engineer', 'Data Scientist', 'DevOps Engineer'): ").strip()
    if not role:
        role = "Software Engineer"
        print(f"   → Using default: {role}")
    
    specialization = input("🔧 Specialization/Focus Area (e.g., 'AI/ML', 'Cloud Infrastructure', 'Frontend Development'): ").strip()
    if not specialization:
        specialization = "Full-stack Development"
        print(f"   → Using default: {specialization}")
    
    experience_level = input("📊 Experience Level (junior/mid-level/senior): ").strip().lower()
    if experience_level not in ['junior', 'mid-level', 'senior']:
        experience_level = "mid-level"
        print(f"   → Using default: {experience_level}")
    
    company_context = input("Company Context (optional - e.g., 'healthcare startup', 'fintech company'): ").strip()
    
    return role, specialization, experience_level, company_context

def generate_behavioral_questions(model, role, specialization, experience_level, company_context=""):
    """Generate behavioral interview questions using advanced prompt engineering"""
    
    context_addition = f" at a {company_context}" if company_context else ""
    
    behavioral_prompt = f"""
You are an experienced technical hiring manager{context_addition}. 
Generate 3 behavioral interview questions specifically designed for a {experience_level} {role} with expertise in {specialization}.

Requirements:
- Questions should assess soft skills crucial for {role}s
- Focus on real scenarios {role}s encounter in {specialization}
- Questions should encourage STAR method responses (Situation, Task, Action, Result)
- Avoid generic questions that could apply to any profession
- Make questions thought-provoking and reveal character/approach
- Tailor questions to {experience_level} experience level

Areas to explore:
- Technical decision-making under pressure
- Collaboration in cross-functional teams
- Handling technical disagreements or conflicts
- Learning and adapting to new technologies in {specialization}
- Mentoring or knowledge sharing experiences (for senior roles)
- Project leadership and ownership (for mid-level+ roles)

Format: Return exactly 3 questions, numbered 1-3.
"""
    
    print(f"BEHAVIORAL QUESTIONS PROMPT FOR {role.upper()} - {specialization.upper()}:")
    print("-" * 70)
    print(behavioral_prompt.strip())
    print(f"\n🤖 GEMINI 2.0 RESPONSE:")
    print("-" * 30)
    
    try:
        response = model.generate_content(behavioral_prompt)
        print(response.text)
        return response.text
    except Exception as e:
        print(f" Error generating behavioral questions: {e}")
        return None

def generate_technical_questions(model, role, specialization, experience_level, company_context=""):
    """Generate technical interview questions using advanced prompt engineering"""
    
    context_addition = f" in a {company_context} environment" if company_context else ""
    
    technical_prompt = f"""
As a senior {role} and technical interviewer with expertise in {specialization},
generate 3 technical interview questions for a {experience_level} {role} specializing in {specialization}{context_addition}.

Requirements:
- Questions should test both theoretical understanding and practical application
- Avoid questions that can be easily googled or memorized
- Include a mix of system design, problem-solving, and implementation concepts
- Questions should be appropriate for {experience_level} candidates
- Focus on real-world {specialization} scenarios and challenges

Question types to include:
1. One system design/architecture question related to {specialization}
2. One algorithmic/problem-solving question with {specialization} context
3. One question about best practices, optimization, or production considerations in {specialization}

Each question should:
- Be specific enough to test deep knowledge in {specialization}
- Allow for follow-up discussions
- Reveal the candidate's experience level and thinking process
- Be relevant to {experience_level} responsibilities

Format: Return exactly 3 questions, numbered 1-3, with brief context for each.
"""
    
    print(f"📝 TECHNICAL QUESTIONS PROMPT FOR {role.upper()} - {specialization.upper()}:")
    print("-" * 70)
    print(technical_prompt.strip())
    print(f"\n🤖 GEMINI 2.0 RESPONSE:")
    print("-" * 30)
    
    try:
        response = model.generate_content(technical_prompt)
        print(response.text)
        return response.text
    except Exception as e:
        print(f"❌ Error generating technical questions: {e}")
        return None

def generate_advanced_context_questions(model, role, specialization, experience_level, company_context):
    """Generate advanced context-aware questions if company context is provided"""
    
    if not company_context:
        return None
    
    advanced_prompt = f"""
Context: You are interviewing for a {experience_level} {role} position at a {company_context} 
that specializes in {specialization}. The company values both technical excellence and 
domain-specific expertise.

Role: Acting as the CTO/Hiring Manager of this {company_context}, create interview questions that assess 
both technical competency and cultural fit for this specific context.

Generate:
- 2 behavioral questions that assess domain awareness and industry-specific considerations
- 2 technical questions specific to {specialization} applications in this industry

Special considerations for {company_context}:
- Industry-specific regulations and compliance requirements
- Domain expertise and understanding of industry challenges
- Ability to work with non-technical stakeholders in this field
- Understanding of ethical considerations specific to this industry

Question characteristics:
- Should differentiate candidates who understand industry-specific challenges
- Test both technical depth and domain awareness
- Assess ethical reasoning and responsibility in technology development
- Evaluate communication skills with domain experts

Format: Clearly separate behavioral and technical questions.
"""
    
    print(f"🚀 ADVANCED CONTEXT-AWARE QUESTIONS FOR {company_context.upper()}:")
    print("-" * 70)
    print(advanced_prompt.strip())
    print(f"\n🤖 GEMINI 2.0 RESPONSE:")
    print("-" * 30)
    
    try:
        response = model.generate_content(advanced_prompt)
        print(response.text)
        return response.text
    except Exception as e:
        print(f"❌ Error generating advanced context questions: {e}")
        return None

def show_prompt_engineering_summary():
    """Display the prompt engineering techniques used"""
    
    print("\n" + "=" * 80)
    print("📚 PROMPT ENGINEERING TECHNIQUES DEMONSTRATED:")
    print("-" * 60)
    
    techniques = """
✅ DYNAMIC ROLE-BASED PROMPTING
   → Adapts persona based on user input (hiring manager, CTO, etc.)
   → Establishes context-specific authority and expertise

✅ PARAMETERIZED CONTEXT INTEGRATION
   → Company context, role, specialization dynamically inserted
   → Industry-specific considerations and compliance requirements
   → Experience level targeting and responsibility alignment

✅ STRUCTURED OUTPUT CONTROL
   → Consistent formatting across all question types
   → "Format: Return exactly 3 questions, numbered 1-3"
   → Clear separation of behavioral and technical questions

✅ CONSTRAINT-BASED PROMPTING
   → "Avoid questions that can be easily googled or memorized"
   → "Avoid generic questions that could apply to any profession"
   → Experience-level appropriate difficulty calibration

✅ MULTI-CRITERIA ASSESSMENT FRAMEWORK
   → Technical competency + cultural fit evaluation
   → Theoretical understanding + practical application balance
   → Ethics + domain expertise integration
   → Communication skills with stakeholders

✅ ADAPTIVE SPECIALIZATION TARGETING
   → Questions tailored to specific technology domains
   → Real-world scenario focus based on specialization
   → Industry-specific best practices and challenges

✅ HIERARCHICAL QUESTION GENERATION
   → Basic behavioral and technical questions
   → Advanced context-aware questions when applicable
   → Progressive complexity based on role seniority
"""
    print(techniques)

def main():
    """Main function demonstrating interactive prompt engineering for interview questions"""
    
    # Configure Gemini AI
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("✅ Successfully connected to Gemini 2.0\n")
    except Exception as e:
        print(f"❌ Error connecting to Gemini: {e}")
        return
    
    # Get user input for role details
    role, specialization, experience_level, company_context = get_user_input()
    
    print("\n" + "=" * 80)
    print("GENERATING CUSTOMIZED INTERVIEW QUESTIONS")
    print(f"Role: {role} | Specialization: {specialization} | Level: {experience_level}")
    if company_context:
        print(f"Context: {company_context}")
    print("=" * 80)
    
    # Generate behavioral questions
    print("\n🎯 BEHAVIORAL INTERVIEW QUESTIONS")
    print("=" * 50)
    behavioral_result = generate_behavioral_questions(model, role, specialization, experience_level, company_context)
    
    # Generate technical questions
    print("\n" + "=" * 80)
    print("\n⚙️ TECHNICAL INTERVIEW QUESTIONS")
    print("=" * 50)
    technical_result = generate_technical_questions(model, role, specialization, experience_level, company_context)
    
    # Generate advanced context-aware questions if context provided
    if company_context:
        print("\n" + "=" * 80)
        advanced_result = generate_advanced_context_questions(model, role, specialization, experience_level, company_context)
    
    # Show prompt engineering techniques summary
    show_prompt_engineering_summary()
    
    # Success summary
    print("\n" + "=" * 80)
    print("✅ INTERVIEW QUESTION GENERATION COMPLETED SUCCESSFULLY")
    print(f"✅ Generated 3 behavioral questions for {role} - {specialization}")
    print(f"✅ Generated 3 technical questions for {experience_level} level")
    if company_context:
        print(f"✅ Generated advanced context-aware questions for {company_context}")
    print("✅ Demonstrated sophisticated prompt engineering techniques")
    print("✅ Used Gemini 2.0 LLM with dynamic prompt generation")
    print("=" * 80)
      # Ask if user wants to generate for another role
    print(f"\n🔄 Would you like to generate questions for another role? (y/n): ", end="")
    if input().strip().lower() in ['y', 'yes']:
        print("\n" + "=" * 80)
        main()  # Recursive call for another round

if __name__ == "__main__":
    main()
