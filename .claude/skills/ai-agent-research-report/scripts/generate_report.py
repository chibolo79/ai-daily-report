#!/usr/bin/env python3
"""
AI Agent Research Report Generator
Generates 2026 AI Agent trend reports with papers, influencers, and company updates.

Usage:
    python generate_report.py [OPTIONS]

Options:
    --papers-only         Generate TOP 5 papers only
    --influencers-only    Generate influencer map only
    --companies-only      Generate company updates only
    --web-search          Use WebSearch (default, ~50-100K tokens)
    --deep-research       Use deep-research workflow (~1.5M tokens)
    --update-html         Regenerate HTML from existing markdown
    --git-commit          Auto-commit to git
    --git-push            Auto-push to origin/master
    --create-issues       Register improvements as GitHub issues
    --output-dir          Output directory (default: current)

Token budgets:
    WebSearch (default): 50-100K - Use for daily/weekly reports
    deep-research: 1.5-2M - Use for quarterly deep-dives only
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """Main report generation orchestrator."""

    def __init__(self, args):
        self.args = args
        self.output_dir = Path(args.output_dir or ".")
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.report_path = self.output_dir / f"{self.today}_AI_Agent_Research_Report"

    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "WARN": "⚠️",
            "ERROR": "❌",
            "SUCCESS": "✅"
        }.get(level, "•")
        print(f"{prefix} [{timestamp}] {message}")

    def run(self):
        """Main execution flow."""
        self.log("Starting AI Agent Research Report generation...")
        self.log(f"Output: {self.report_path}")
        self.log(f"Search mode: {self.get_search_mode()}")
        self.log(f"Token budget: {self.get_token_budget()}")

        try:
            # Step 1: Determine what to generate
            sections = self._get_sections_to_generate()
            self.log(f"Generating sections: {', '.join(sections)}")

            # Step 2: Collect data
            data = {}
            if "papers" in sections:
                data["papers"] = self._generate_papers_section()
            if "influencers" in sections:
                data["influencers"] = self._generate_influencers_section()
            if "companies" in sections:
                data["companies"] = self._generate_companies_section()

            # Step 3: Generate markdown
            if not self.args.update_html:
                markdown_path = self._generate_markdown(data, sections)
                self.log(f"Markdown generated: {markdown_path}", "SUCCESS")
            else:
                markdown_path = self._find_existing_markdown()
                if not markdown_path:
                    self.log("No existing markdown found for --update-html", "ERROR")
                    return False

            # Step 4: Generate HTML
            html_path = self._generate_html(markdown_path)
            self.log(f"HTML generated: {html_path}", "SUCCESS")

            # Step 5: Git operations (optional)
            if self.args.git_commit:
                self._git_commit(markdown_path, html_path)
            if self.args.git_push:
                self._git_push()

            # Step 6: Create issues (optional)
            if self.args.create_issues:
                self._create_issues()

            self.log("Report generation completed successfully!", "SUCCESS")
            return True

        except Exception as e:
            self.log(f"Error: {str(e)}", "ERROR")
            return False

    def get_search_mode(self) -> str:
        """Return current search mode."""
        return "deep-research" if self.args.deep_research else "web-search"

    def get_token_budget(self) -> str:
        """Return estimated token budget."""
        if self.args.papers_only:
            return "20-30K"
        elif self.args.deep_research:
            return "1.5-2M"
        else:
            return "50-100K"

    def _get_sections_to_generate(self) -> list:
        """Determine which sections to generate."""
        sections = []
        if self.args.papers_only:
            sections = ["papers"]
        elif self.args.influencers_only:
            sections = ["influencers"]
        elif self.args.companies_only:
            sections = ["companies"]
        else:
            sections = ["papers", "influencers", "companies"]
        return sections

    def _generate_papers_section(self) -> dict:
        """Generate TOP 5 papers section."""
        self.log("Collecting papers data...")
        # In actual implementation, this would call WebSearch or deep-research
        # For now, returning template structure
        return {
            "title": "2026 AI Agent 핵심 논문 TOP 5",
            "papers": [
                {
                    "rank": 1,
                    "title": "GLEAN: Guideline-Grounded Evidence Accumulation",
                    "authors": "Mihaela van der Schaar Lab et al.",
                    "venue": "ICLR 2026 Workshop",
                    "date": "2026-03",
                    "reason": "고위험 도메인 검증 신뢰성",
                    "idea": "가이드라인 기반 증거 누적 검증",
                    "application": "의료·법률·금융 에이전트 검증"
                }
                # More papers would be added here
            ]
        }

    def _generate_influencers_section(self) -> dict:
        """Generate influencer map section."""
        self.log("Collecting influencer data...")
        return {
            "title": "주목 인플루언서 & 커뮤니티",
            "reddit": [
                {"name": "r/LocalLLaMA", "reason": "오픈소스 LLM 실무"},
                {"name": "r/MachineLearning", "reason": "논문 기반 토론"},
                {"name": "r/LangChain", "reason": "에이전트 구현"}
            ],
            "twitter": [
                {"name": "@karpathy", "reason": "LLM 원리 설명"},
                {"name": "@simonw", "reason": "실무 LLM 활용"},
                {"name": "@swyx", "reason": "AI Engineer 생태계"}
            ]
        }

    def _generate_companies_section(self) -> dict:
        """Generate company updates section."""
        self.log("Collecting company updates...")
        return {
            "title": "기업 업데이트 이력",
            "companies": {
                "anthropic": "Claude 3.x, Computer Use, MCP, Claude Code, Extended Thinking",
                "openai": "GPT-4o, o3/o4, Operator, Deep Research, Responses API",
                "google": "Gemini 2.0+, Project Astra, Agentspace, Jules"
            }
        }

    def _generate_markdown(self, data: dict, sections: list) -> Path:
        """Generate markdown file from collected data."""
        self.log("Generating markdown...")
        markdown_path = self.report_path.with_suffix(".md")

        content = f"""# 2026 AI Agent 트렌드 리서치 리포트

**작성일**: {self.today}
**검색 방식**: {self.get_search_mode()}
**토큰 사용**: {self.get_token_budget()}

---

"""

        # Add sections
        for section in sections:
            if section == "papers" and "papers" in data:
                content += self._format_papers_markdown(data["papers"])
            elif section == "influencers" and "influencers" in data:
                content += self._format_influencers_markdown(data["influencers"])
            elif section == "companies" and "companies" in data:
                content += self._format_companies_markdown(data["companies"])

        # Write file
        markdown_path.write_text(content, encoding="utf-8")
        return markdown_path

    def _format_papers_markdown(self, papers: dict) -> str:
        """Format papers section as markdown."""
        md = f"## {papers['title']}\n\n"
        for paper in papers.get("papers", []):
            md += f"### {paper['rank']}위: {paper['title']}\n"
            md += f"- **저자**: {paper['authors']}\n"
            md += f"- **발표**: {paper['venue']}\n"
            md += f"- **선정**: {paper['reason']}\n"
            md += f"- **아이디어**: {paper['idea']}\n"
            md += f"- **활용**: {paper['application']}\n\n"
        return md

    def _format_influencers_markdown(self, influencers: dict) -> str:
        """Format influencers section as markdown."""
        md = f"## {influencers['title']}\n\n"
        md += "### Reddit\n"
        for sub in influencers.get("reddit", []):
            md += f"- **{sub['name']}**: {sub['reason']}\n"
        md += "\n### X (Twitter)\n"
        for acc in influencers.get("twitter", []):
            md += f"- **{acc['name']}**: {acc['reason']}\n"
        return md

    def _format_companies_markdown(self, companies: dict) -> str:
        """Format companies section as markdown."""
        md = f"## {companies['title']}\n\n"
        for company, updates in companies.get("companies", {}).items():
            md += f"### {company.upper()}\n{updates}\n\n"
        return md

    def _generate_html(self, markdown_path: Path) -> Path:
        """Convert markdown to HTML."""
        self.log("Generating HTML...")
        html_path = markdown_path.with_suffix(".html")

        # Read markdown
        md_content = markdown_path.read_text(encoding="utf-8")

        # Simple HTML template (in production, use proper markdown library)
        html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026 AI Agent 트렌드 리서치 리포트</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        h1 {{ color: #667eea; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
        h2 {{ color: #764ba2; margin-top: 30px; }}
        h3 {{ color: #666; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #667eea; color: white; }}
        tr:hover {{ background: #f8f9ff; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        .meta {{ background: #e8eaf6; padding: 15px; border-radius: 6px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>2026 AI Agent 트렌드 리서치 리포트</h1>
        <div class="meta">
            <strong>작성일:</strong> {self.today}<br>
            <strong>검색 방식:</strong> {self.get_search_mode()}<br>
            <strong>토큰 사용:</strong> {self.get_token_budget()}
        </div>
        {self._markdown_to_html_simple(md_content)}
    </div>
</body>
</html>"""

        html_path.write_text(html_content, encoding="utf-8")
        return html_path

    def _markdown_to_html_simple(self, md: str) -> str:
        """Simple markdown to HTML conversion."""
        # In production, use proper library like markdown2 or mistune
        html = md.replace("\n\n", "</p><p>")
        html = html.replace("# ", "<h1>").replace("\n", "</h1>\n")
        html = html.replace("## ", "<h2>").replace("\n", "</h2>\n")
        html = html.replace("### ", "<h3>").replace("\n", "</h3>\n")
        html = html.replace("- ", "<li>").replace("\n", "</li>\n")
        html = f"<p>{html}</p>"
        return html

    def _find_existing_markdown(self) -> Path:
        """Find most recent markdown file."""
        md_files = list(self.output_dir.glob("*_AI_Agent_Research_Report.md"))
        if not md_files:
            return None
        return sorted(md_files)[-1]  # Return most recent

    def _git_commit(self, markdown_path: Path, html_path: Path):
        """Commit changes to git."""
        self.log("Committing to git...")
        try:
            subprocess.run(
                ["git", "add", str(markdown_path), str(html_path)],
                cwd=self.output_dir,
                check=True,
                capture_output=True
            )
            subprocess.run(
                ["git", "commit", "-m", f"Update AI Agent research report ({self.today})"],
                cwd=self.output_dir,
                check=True,
                capture_output=True
            )
            self.log("Git commit successful", "SUCCESS")
        except subprocess.CalledProcessError as e:
            self.log(f"Git commit failed: {e}", "WARN")

    def _git_push(self):
        """Push to remote repository."""
        self.log("Pushing to GitHub...")
        try:
            subprocess.run(
                ["git", "push", "origin", "master"],
                cwd=self.output_dir,
                check=True,
                capture_output=True
            )
            self.log("Git push successful", "SUCCESS")
        except subprocess.CalledProcessError as e:
            self.log(f"Git push failed: {e}", "WARN")

    def _create_issues(self):
        """Create GitHub issues for identified improvements."""
        self.log("Creating GitHub issues...")
        self.log("Note: Issues should be created with proper GitHub API", "WARN")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate 2026 AI Agent Research Report"
    )
    parser.add_argument("--papers-only", action="store_true", help="Generate papers only")
    parser.add_argument("--influencers-only", action="store_true", help="Generate influencers only")
    parser.add_argument("--companies-only", action="store_true", help="Generate companies only")
    parser.add_argument("--web-search", action="store_true", default=True, help="Use WebSearch (default)")
    parser.add_argument("--deep-research", action="store_true", help="Use deep-research workflow")
    parser.add_argument("--update-html", action="store_true", help="Regenerate HTML only")
    parser.add_argument("--git-commit", action="store_true", help="Auto-commit to git")
    parser.add_argument("--git-push", action="store_true", help="Auto-push to GitHub")
    parser.add_argument("--create-issues", action="store_true", help="Create GitHub issues")
    parser.add_argument("--output-dir", help="Output directory")

    args = parser.parse_args()

    generator = ReportGenerator(args)
    success = generator.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
