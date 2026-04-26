"""
Report Generation Module
"""
from datetime import datetime
from jinja2 import Template
import os

class ReportGenerator:
    """Generate PDF and HTML reports"""
    
    def __init__(self):
        self.report_dir = 'reports'
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)
    
    def generate_html_report(self, case_data, analytics_data):
        """Generate HTML report"""
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Social Media Analytics Report - {{ case_name }}</title>
            <style>
                * { margin: 0; padding: 0; }
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
                header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; border-radius: 8px; margin-bottom: 30px; }
                h1 { font-size: 2.5em; margin-bottom: 10px; }
                .subtitle { font-size: 1.1em; opacity: 0.9; }
                .section { background: white; padding: 30px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h2 { color: #667eea; border-bottom: 3px solid #667eea; padding-bottom: 10px; margin-bottom: 20px; }
                .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
                .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }
                .metric-value { font-size: 2em; font-weight: bold; }
                .metric-label { font-size: 0.9em; opacity: 0.9; margin-top: 10px; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th { background: #667eea; color: white; padding: 12px; text-align: left; }
                td { padding: 12px; border-bottom: 1px solid #ddd; }
                tr:hover { background: #f5f5f5; }
                footer { text-align: center; padding: 20px; color: #999; font-size: 0.9em; }
                .chart-placeholder { background: #f9f9f9; padding: 20px; text-align: center; border: 2px dashed #ddd; border-radius: 8px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <header>
                    <h1>Social Media Analytics Report</h1>
                    <p class="subtitle">{{ case_name }} - {{ platform }}</p>
                    <p>Generated on {{ date }}</p>
                </header>
                
                <div class="section">
                    <h2>Executive Summary</h2>
                    <div class="metrics">
                        <div class="metric-card">
                            <div class="metric-value">{{ total_posts }}</div>
                            <div class="metric-label">Total Posts</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{{ total_engagement }}</div>
                            <div class="metric-label">Total Engagement</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{{ avg_engagement | round(2) }}</div>
                            <div class="metric-label">Avg Engagement</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Sentiment Analysis</h2>
                    <div class="metrics">
                        <div class="metric-card">
                            <div class="metric-value" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">{{ sentiment_positive }}</div>
                            <div class="metric-label">Positive</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value" style="background: linear-gradient(135deg, #F093FB 0%, #F5576C 100%);">{{ sentiment_negative }}</div>
                            <div class="metric-label">Negative</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">{{ sentiment_neutral }}</div>
                            <div class="metric-label">Neutral</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Top Trending Topics</h2>
                    {% if trends %}
                    <table>
                        <tr>
                            <th>Hashtag</th>
                            <th>Frequency</th>
                            <th>Trend Score</th>
                        </tr>
                        {% for trend in trends[:10] %}
                        <tr>
                            <td>{{ trend.hashtag }}</td>
                            <td>{{ trend.frequency }}</td>
                            <td>{{ trend.trend_score | round(3) }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                    {% else %}
                    <p>No trending topics detected.</p>
                    {% endif %}
                </div>
                
                <div class="section">
                    <h2>Top Influencers</h2>
                    {% if influencers %}
                    <table>
                        <tr>
                            <th>Username</th>
                            <th>Followers</th>
                            <th>Engagement Rate</th>
                            <th>Tier</th>
                        </tr>
                        {% for influencer in influencers[:10] %}
                        <tr>
                            <td>{{ influencer.username }}</td>
                            <td>{{ influencer.followers }}</td>
                            <td>{{ influencer.engagement_rate | round(3) }}</td>
                            <td>{{ influencer.influence_tier }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                    {% else %}
                    <p>No influencers detected.</p>
                    {% endif %}
                </div>
                
                <footer>
                    <p>&copy; 2024 Social Media Analytics Application. All rights reserved.</p>
                </footer>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            case_name=case_data.get('name', 'Unknown'),
            platform=case_data.get('platform', 'Unknown'),
            date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_posts=analytics_data.get('total_posts', 0),
            total_engagement=analytics_data.get('total_engagement', 0),
            avg_engagement=analytics_data.get('avg_engagement', 0),
            sentiment_positive=analytics_data.get('sentiment', {}).get('positive', 0),
            sentiment_negative=analytics_data.get('sentiment', {}).get('negative', 0),
            sentiment_neutral=analytics_data.get('sentiment', {}).get('neutral', 0),
            trends=analytics_data.get('trends', []),
            influencers=analytics_data.get('influencers', [])
        )
        
        return html_content
    
    def save_report(self, filename, content):
        """Save report to file"""
        filepath = os.path.join(self.report_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
