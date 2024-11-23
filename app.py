from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
import plotly.graph_objects as go  # Add this import
import os
from sqlalchemy import func
from flask_login import current_user  # Add this import at the top of your file

# Define the constants here, before creating the Flask app
LOGGED_IN_HEADER_STYLE = '''
    header {
        background-color: var(--header-bg);
        position: fixed;
        width: 100%;
        height: 70px;
        top: 0;
        left: 0;
        z-index: 1000;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    nav {
        position: relative;
        width: 1200px;
        height: 100%;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .logo {
        position: absolute;
        left: 20px;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-light);
        text-decoration: none;
    }

    .logo span {
        color: var(--primary-color);
    }

    .nav-links {
        position: absolute;
        right: 20px;
        display: flex;
        align-items: center;
    }

    .nav-links a {
        color: var(--text-light);
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 0.5rem 1rem;
        margin: 0 0.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .nav-links a:hover {
        color: var(--primary-color);
        background: rgba(255, 215, 0, 0.1);
    }

    .nav-links a.login {
        background: var(--primary-color);
        color: #000000;
        font-weight: 600;
        margin-left: 1rem;
    }

    .content-wrapper {
        padding-top: 90px;
    }
'''

LOGGED_IN_HEADER = '''
    <header>
        <nav>
            <a href="/" class="logo">Know Your <span>$avings</span></a>
            <div class="nav-links">
                <a href="/dashboard">Dashboard</a>
                <a href="/wallets">Wallets</a>
                <a href="/budgets">Budgets</a>
                <a href="/reports">Reports</a>
                <a href="/settings">Settings</a>
                <a href="/logout" class="login">Logout</a>
            </div>
        </nav>
    </header>
'''

# Then continue with your Flask app initialization
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'wallets.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    wallet_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    transactions = db.relationship('Transaction', backref='wallet', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_type = db.Column(db.String(50))  # 'deposit', 'withdrawal', 'transfer'

# Add this to your database models
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)  # 'Income', 'Savings', 'Expenses'
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    current_amount = db.Column(db.Float, default=0.0)
    period = db.Column(db.String(20), default='Monthly')  # Monthly, Weekly, Yearly
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

def create_graph():
    fig = go.Figure()
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    income = [4500, 4800, 4700, 4850, 4900, 5100]
    expenses = [3800, 3900, 3850, 3700, 3800, 3900]

    fig.add_trace(go.Scatter(
        x=months,
        y=income,
        name='Income',
        line=dict(color='#FFD700', width=3, shape='spline'),
        mode='lines+markers'
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=expenses,
        name='Expenses',
        line=dict(color='#94A3B8', width=3, shape='spline'),
        mode='lines+markers'
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        margin=dict(l=40, r=20, t=20, b=40),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='rgba(255,255,255,0.1)',
            fixedrange=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            showline=True,
            linecolor='rgba(255,255,255,0.1)',
            fixedrange=True
        ),
        dragmode=False
    )
    
    config = {
        'displayModeBar': False,
        'staticPlot': True
    }
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn', config=config)

def create_spending_graph():
    fig = go.Figure()
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    categories = ['Bills', 'Shopping', 'Food', 'Transport']
    expenses = [1200, 950, 1100, 880, 1050, 920]
    
    for i, category in enumerate(categories):
        fig.add_trace(go.Bar(
            name=category,
            x=months,
            y=[expenses[j] * (0.1 + i * 0.2) for j in range(len(months))],
            marker_color=['#FFD700', '#FFC700', '#FFB700', '#FFA700'][i]
        ))

    fig.update_layout(
        barmode='stack',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        margin=dict(l=40, r=20, t=20, b=40),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='rgba(255,255,255,0.1)',
            fixedrange=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            showline=True,
            linecolor='rgba(255,255,255,0.1)',
            fixedrange=True
        ),
        dragmode=False
    )
    
    config = {
        'displayModeBar': False,
        'staticPlot': True
    }
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn', config=config)

def create_savings_graph():
    fig = go.Figure()
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    savings = [5000, 5600, 6400, 7500, 8900, 10500]
    goal_line = [12000] * len(months)
    
    fig.add_trace(go.Scatter(
        x=months,
        y=savings,
        mode='lines+markers',
        name='Savings',
        line=dict(color='#FFD700', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=goal_line,
        mode='lines',
        name='Goal',
        line=dict(color='#94A3B8', width=2, dash='dash')
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        margin=dict(l=40, r=20, t=20, b=40),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='rgba(255,255,255,0.1)',
            fixedrange=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            showline=True,
            linecolor='rgba(255,255,255,0.1)',
            fixedrange=True
        ),
        dragmode=False
    )
    
    config = {
        'displayModeBar': False,
        'staticPlot': True
    }
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn', config=config)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    expense_graph = create_graph()  # Original graph for step 1
    spending_graph = create_spending_graph()  # New graph for step 2
    savings_graph = create_savings_graph()  # New graph for step 3
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>FinanceTracker</title>
        <style>
            :root {
                --primary-color: #FFD700;
                --primary-dark: #FFC700;
                --accent-color: #FFB700;
                --header-bg: #0A1929;
                --bg-dark: #000000;
                --bg-darker: #000000;
                --text-light: #ffffff;
                --text-muted: #94A3B8;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                background-color: var(--bg-dark);
                color: var(--text-light);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                line-height: 1.6;
            }
            
            header {
                background-color: var(--header-bg);
                position: fixed;
                width: 100%;
                height: 70px;  /* Fixed height */
                top: 0;
                left: 0;
                z-index: 1000;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            nav {
                position: relative;
                width: 1200px;  /* Fixed width */
                height: 100%;
                margin: 0 auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .logo {
                position: absolute;
                left: 20px;
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--text-light);
                text-decoration: none;
            }
            
            .logo span {
                color: var(--primary-color);
            }
            
            .nav-links {
                position: absolute;
                right: 20px;
                display: flex;
                align-items: center;
            }
            
            .nav-links a {
                color: var(--text-light);
                text-decoration: none;
                font-weight: 500;
                font-size: 0.95rem;
                padding: 0.5rem 1rem;
                margin: 0 0.5rem;  /* Fixed margins */
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            
            .nav-links a:hover {
                color: var(--primary-color);
                background: rgba(255, 215, 0, 0.1);
            }
            
            .nav-links a.login {
                background: var(--primary-color);
                color: #000000;
                font-weight: 600;
                margin-left: 1rem;  /* Fixed margin */
            }
            
            .nav-links a.signup {
                background: transparent;
                color: var(--primary-color);
                font-weight: 600;
                border: 2px solid var(--primary-color);
            }
            
            .nav-links a.signup:hover {
                background: rgba(255, 215, 0, 0.1);
                color: var(--primary-color);
            }
            
            .hero {
                padding: 140px 20px 60px;
                text-align: center;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .hero-title {
                font-size: 3.5rem;
                margin-bottom: 1rem;
                line-height: 1.2;
            }
            
            .hero-title span {
                color: var(--primary-color);
            }
            
            .hero-subtitle {
                color: var(--text-muted);
                font-size: 1.2rem;
                max-width: 600px;
                margin: 0 auto 2rem;
            }
            
            .button {
                display: inline-block;
                background: var(--primary-color);
                color: #000000;
                padding: 0.8rem 1.5rem;
                border-radius: 8px;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .button:hover {
                background: var(--primary-dark);
                transform: translateY(-2px);
            }
            
            .features-section {
                padding: 80px 20px;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .section-title {
                text-align: center;
                font-size: 2.5rem;
                margin-bottom: 3rem;
            }
            
            .section-title span {
                color: var(--primary-color);
            }
            
            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
            }
            
            .feature-item {
                background: var(--header-bg);
                padding: 2rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .feature-icon {
                font-size: 2rem;
                margin-bottom: 1rem;
            }
            
            .feature-name {
                font-size: 1.5rem;
                margin-bottom: 1rem;
                color: var(--text-light);
            }
            
            .feature-desc {
                color: var(--text-muted);
                margin-bottom: 1.5rem;
            }
            
            .feature-details ul {
                list-style: none;
                color: var(--text-muted);
            }
            
            .feature-details li {
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .feature-details li::before {
                content: "•";
                color: var(--primary-color);
            }
            
            .steps-section {
                padding: 80px 20px;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .step-container {
                display: flex;
                align-items: center;
                gap: 4rem;
                margin-bottom: 4rem;
                background: var(--header-bg);
                padding: 2rem;
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .step-container.reverse {
                flex-direction: row-reverse;
            }
            
            .step-content {
                flex: 1;
            }
            
            .step-number {
                color: var(--primary-color);
                font-size: 1.2rem;
                margin-bottom: 0.5rem;
            }
            
            .step-title {
                font-size: 2rem;
                margin-bottom: 1rem;
            }
            
            .step-features {
                list-style: none;
                color: var(--text-muted);
            }
            
            .step-features li {
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .step-features li::before {
                content: "•";
                color: var(--primary-color);
            }
            
            .step-visual {
                flex: 1;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 15px;
                padding: 2rem;
            }
            
            .advanced-section {
                padding: 80px 20px;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .advanced-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
            }
            
            .advanced-item {
                position: relative;
                height: 300px;
                border-radius: 15px;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
                padding: 2rem;
                color: var(--text-light);
                transition: transform 0.3s ease;
            }
            
            .advanced-item:hover {
                transform: translateY(-5px);
            }
            
            .advanced-item::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(to top, rgba(0,0,0,0.9) 20%, rgba(0,0,0,0.5) 50%, rgba(0,0,0,0.3) 100%);
                z-index: 1;
            }
            
            .advanced-item.portfolio {
                background: url('https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80') center/cover;
            }
            
            .advanced-item.reports {
                background: url('https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80') center/cover;
            }
            
            .advanced-item.wealth {
                background: url('https://images.unsplash.com/photo-1579621970588-a35d0e7ab9b6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80') center/cover;
            }
            
            .advanced-item.currency {
                background: url('https://images.unsplash.com/photo-1580519542036-c47de6196ba5?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80') center/cover;
            }
            
            .advanced-content {
                position: relative;
                z-index: 2;
            }
            
            .advanced-icon {
                font-size: 2.5rem;
                margin-bottom: 1rem;
            }
            
            .advanced-name {
                font-size: 1.5rem;
                margin-bottom: 0.5rem;
                font-weight: 600;
            }
            
            .advanced-desc {
                color: var(--text-muted);
            }
        </style>
    </head>
    <body>
        <header>
            <nav>
                <a href="/" class="logo">Know Your <span>$avings</span></a>
                <div class="nav-links">
                    <a href="/">Home</a>
                    <a href="/features">Features</a>
                    <a href="/pricing">Pricing</a>
                    <a href="/login" class="login">Login</a>
                </div>
            </nav>
        </header>

        <section class="hero">
            <div class="hero-content">
                <h1 class="hero-title">Powerful data insights <span>for everyone</span></h1>
                <p class="hero-subtitle">Know Your Savings helps you track, compare, and optimize your finances effortlessly by showing you how much you can save on bills, subscriptions, insurance, and more</p>
                <a href="/signup" class="button">Sign up here</a>
            </div>
        </section>

        <section class="steps-section">
            <h2 class="section-title">Your Path to <span>Financial Success</span></h2>
            
            <div class="step-container">
                <div class="step-content">
                    <h3 class="step-number">Step 1</h3>
                    <h3 class="step-title">Track your cash flow</h3>
                    <ul class="step-features">
                        <li>Connect your bank accounts for automatic tracking</li>
                        <li>Track all your expenses in one place</li>
                        <li>Manage multiple wallets and accounts</li>
                    </ul>
                </div>
                <div class="step-visual">
                    {{ expense_graph|safe }}
                </div>
            </div>

            <div class="step-container reverse">
                <div class="step-content">
                    <h3 class="step-number">Step 2</h3>
                    <h3 class="step-title">Understand your financial habits</h3>
                    <ul class="step-features">
                        <li>Analyze your finances with beautiful graphics</li>
                        <li>Track where your money goes each month</li>
                        <li>Get instant insights into your spending patterns</li>
                    </ul>
                </div>
                <div class="step-visual">
                    {{ spending_graph|safe }}
                </div>
            </div>

            <div class="step-container">
                <div class="step-content">
                    <h3 class="step-number">Step 3</h3>
                    <h3 class="step-title">Make your spending stress-free</h3>
                    <ul class="step-features">
                        <li>Set smart budgets for different categories</li>
                        <li>Track daily spending limits</li>
                        <li>Save money for your future goals</li>
                    </ul>
                </div>
                <div class="step-visual">
                    {{ savings_graph|safe }}
                </div>
            </div>
        </section>

        <section class="features-section">
            <h2 class="section-title">Features that make a difference</h2>
            <div class="features-grid">
                <div class="feature-item">
                    <div class="feature-icon">📊</div>
                    <h3 class="feature-name">Portfolio Analysis</h3>
                    <p class="feature-desc">Track and analyze your investments</p>
                    <div class="feature-details">
                        <ul>
                            <li>Real-time investment tracking</li>
                            <li>Performance analytics</li>
                            <li>Asset allocation insights</li>
                            <li>Investment recommendations</li>
                        </ul>
                    </div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">💰</div>
                    <h3 class="feature-name">Smart Budgeting</h3>
                    <p class="feature-desc">Take control of your spending</p>
                    <div class="feature-details">
                        <ul>
                            <li>Automated categorization</li>
                            <li>Custom budget templates</li>
                            <li>Spending limits</li>
                            <li>Budget notifications</li>
                        </ul>
                    </div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">📈</div>
                    <h3 class="feature-name">Wealth Tracking</h3>
                    <p class="feature-desc">Monitor your financial growth</p>
                    <div class="feature-details">
                        <ul>
                            <li>Net worth calculations</li>
                            <li>Goal progress tracking</li>
                            <li>Future projections</li>
                            <li>Growth analytics</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <section class="advanced-section">
            <h2 class="section-title">Advanced Tools</h2>
            <div class="advanced-grid">
                <div class="advanced-item portfolio">
                    <div class="advanced-content">
                        <div class="advanced-icon">📊</div>
                        <h3 class="advanced-name">Portfolio Analysis</h3>
                        <p class="advanced-desc">Track and analyze your investments</p>
                    </div>
                </div>
                <div class="advanced-item reports">
                    <div class="advanced-content">
                        <div class="advanced-icon">📈</div>
                        <h3 class="advanced-name">Reports & Insights</h3>
                        <p class="advanced-desc">Detailed financial analysis</p>
                    </div>
                </div>
                <div class="advanced-item wealth">
                    <div class="advanced-content">
                        <div class="advanced-icon">💰</div>
                        <h3 class="advanced-name">Wealth Tracking</h3>
                        <p class="advanced-desc">Monitor your financial growth</p>
                    </div>
                </div>
                <div class="advanced-item currency">
                    <div class="advanced-content">
                        <div class="advanced-icon">🌐</div>
                        <h3 class="advanced-name">Multi-Currency</h3>
                        <p class="advanced-desc">Global finance management</p>
                    </div>
                </div>
            </div>
        </section>
    </body>
    </html>
    ''', expense_graph=expense_graph, spending_graph=spending_graph, savings_graph=savings_graph)

@app.route('/wallets')
@login_required
def wallets():
    user_wallets = Wallet.query.all()
    
    # Convert wallets to a list of dictionaries
    wallets_list = [
        {
            'id': wallet.id,
            'name': wallet.name,
            'type': wallet.wallet_type,
            'balance': float(wallet.balance)
        } for wallet in user_wallets
    ]
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Wallets - Know Your $avings</title>
        <style>
            :root {
                --primary-color: #FFD700;
                --primary-dark: #FFC700;
                --accent-color: #FFB700;
                --header-bg: #0A1929;
                --bg-dark: #000000;
                --bg-lighter: #1A2027;
                --text-light: #ffffff;
                --text-muted: #94A3B8;
                --card-bg: #0A1929;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 0;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: var(--bg-dark);
                color: var(--text-light);
                line-height: 1.6;
            }
            
            ''' + LOGGED_IN_HEADER_STYLE + '''

            .wallets-content {
                padding: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }

            .welcome-header {
                margin-bottom: 2rem;
            }

            .welcome-title {
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }

            .welcome-subtitle {
                color: var(--text-muted);
            }

            .header-actions {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 2rem;
            }

            .wallets-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }

            .wallet-card {
                background: var(--header-bg);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                cursor: pointer;
                transition: transform 0.2s ease;
            }

            .wallet-card:hover {
                transform: translateY(-2px);
            }

            .wallet-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }

            .wallet-name {
                font-size: 1.2rem;
                font-weight: 600;
            }

            .wallet-type {
                color: var(--text-muted);
                font-size: 0.9rem;
            }

            .wallet-balance {
                font-size: 2rem;
                font-weight: 600;
                margin: 1rem 0;
            }

            .wallet-actions {
                display: flex;
                gap: 1rem;
            }

            .action-button {
                padding: 0.5rem 1rem;
                border: none;
                border-radius: 8px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 0.95rem;
            }

            .primary-button {
                background: var(--primary-color);
                color: #000000;
                font-weight: 600;
            }

            .secondary-button {
                background: rgba(255, 255, 255, 0.1);
                color: var(--text-light);
                font-weight: 500;
            }

            .action-button:hover {
                transform: translateY(-2px);
            }

            /* Modal styles */
            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                z-index: 1001;
            }

            .modal-content {
                background: var(--header-bg);
                padding: 2rem;
                border-radius: 15px;
                width: 90%;
                max-width: 500px;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            .modal-title {
                margin-bottom: 1.5rem;
                font-size: 1.5rem;
            }

            .form-group {
                margin-bottom: 1rem;
            }

            .form-group label {
                display: block;
                margin-bottom: 0.5rem;
                color: var(--text-muted);
            }

            .form-group input, .form-group select {
                width: 100%;
                padding: 0.5rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.05);
                color: var(--text-light);
                font-family: inherit;
            }

            .modal-actions {
                display: flex;
                justify-content: flex-end;
                gap: 1rem;
                margin-top: 1.5rem;
            }

            .close-button {
                position: absolute;
                right: 1rem;
                top: 1rem;
                background: none;
                border: none;
                color: var(--text-muted);
                cursor: pointer;
                font-size: 1.5rem;
            }
        </style>
    </head>
    <body>
        ''' + LOGGED_IN_HEADER + '''
        <div class="content-wrapper">
            <div class="wallets-content">
                <div class="welcome-header">
                    <h1 class="welcome-title">Your Wallets</h1>
                    <p class="welcome-subtitle">Manage and track your finances</p>
                </div>

                <div class="header-actions">
                    <button class="action-button primary-button" onclick="showNewWalletModal()">Add New Wallet</button>
                </div>

                <div class="wallets-grid">
                    {% for wallet in wallets %}
                    <div class="wallet-card" onclick="editWallet({{ {
                        'id': wallet.id,
                        'name': wallet.name,
                        'type': wallet.wallet_type,
                        'balance': wallet.balance
                    }|tojson }})">
                        <div class="wallet-header">
                            <div>
                                <h3 class="wallet-name">{{ wallet.name }}</h3>
                                <span class="wallet-type">{{ wallet.wallet_type }}</span>
                            </div>
                        </div>
                        <div class="wallet-balance">${{ "%.2f"|format(wallet.balance) }}</div>
                        <div class="wallet-actions">
                            <button class="action-button primary-button" onclick="showAddFundsModal('{{ wallet.id }}')">Add Funds</button>
                            <button class="action-button secondary-button" onclick="showTransferModal('{{ wallet.id }}')">Transfer</button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- New Wallet Modal -->
        <div id="newWalletModal" class="modal">
            <div class="modal-content">
                <button class="close-button" onclick="closeModal('newWalletModal')">&times;</button>
                <h2 class="modal-title">Add New Wallet</h2>
                <form action="{{ url_for('add_wallet') }}" method="POST">
                    <div class="form-group">
                        <label for="name">Wallet Name</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="type">Wallet Type</label>
                        <select id="type" name="type" required>
                            <option value="Cash">Cash</option>
                            <option value="Bank">Bank Account</option>
                            <option value="Credit">Credit Card</option>
                            <option value="Investment">Investment</option>
                        </select>
                    </div>
                    <div class="modal-actions">
                        <button type="button" class="action-button secondary-button" onclick="closeModal('newWalletModal')">Cancel</button>
                        <button type="submit" class="action-button primary-button">Add Wallet</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Add Funds Modal -->
        <div id="addFundsModal" class="modal">
            <div class="modal-content">
                <button class="close-button" onclick="closeModal('addFundsModal')">&times;</button>
                <h2 class="modal-title">Add Funds</h2>
                <form action="{{ url_for('add_funds') }}" method="POST">
                    <input type="hidden" id="add_funds_wallet_id" name="wallet_id">
                    <div class="form-group">
                        <label for="amount">Amount</label>
                        <input type="number" id="amount" name="amount" step="0.01" required>
                    </div>
                    <div class="modal-actions">
                        <button type="button" class="action-button secondary-button" onclick="closeModal('addFundsModal')">Cancel</button>
                        <button type="submit" class="action-button primary-button">Add Funds</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Transfer Modal -->
        <div id="transferModal" class="modal">
            <div class="modal-content">
                <button class="close-button" onclick="closeModal('transferModal')">&times;</button>
                <h2 class="modal-title">Transfer Funds</h2>
                <form action="{{ url_for('transfer_funds') }}" method="POST">
                    <input type="hidden" id="from_wallet" name="from_wallet">
                    <div class="form-group">
                        <label for="to_wallet">To Wallet</label>
                        <select id="to_wallet" name="to_wallet" required>
                            {% for wallet in wallets %}
                            <option value="{{ wallet.id }}">{{ wallet.name }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="transfer_amount">Amount</label>
                        <input type="number" id="transfer_amount" name="amount" step="0.01" required>
                    </div>
                    <div class="modal-actions">
                        <button type="button" class="action-button secondary-button" onclick="closeModal('transferModal')">Cancel</button>
                        <button type="submit" class="action-button primary-button">Transfer</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Edit Wallet Modal -->
        <div id="editWalletModal" class="modal">
            <div class="modal-content">
                <button class="close-button" onclick="closeModal('editWalletModal')">&times;</button>
                <h2 class="modal-title">Edit Wallet</h2>
                <form action="" method="POST" id="editWalletForm">
                    <div class="form-group">
                        <label for="edit_name">Wallet Name</label>
                        <input type="text" id="edit_name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="edit_type">Wallet Type</label>
                        <select id="edit_type" name="type" required>
                            <option value="Cash">Cash</option>
                            <option value="Bank">Bank Account</option>
                            <option value="Credit">Credit Card</option>
                            <option value="Investment">Investment</option>
                        </select>
                    </div>
                    <div class="modal-actions">
                        <button type="button" class="action-button secondary-button" onclick="deleteWallet()">Delete</button>
                        <button type="submit" class="action-button primary-button">Update</button>
                    </div>
                </form>
            </div>
        </div>

        <script>
            function showModal(modalId) {
                document.getElementById(modalId).style.display = 'block';
            }

            function closeModal(modalId) {
                document.getElementById(modalId).style.display = 'none';
            }

            function showNewWalletModal() {
                showModal('newWalletModal');
            }

            function showAddFundsModal(walletId) {
                event.stopPropagation();
                document.getElementById('add_funds_wallet_id').value = walletId;
                showModal('addFundsModal');
            }

            function showTransferModal(walletId) {
                event.stopPropagation();
                document.getElementById('from_wallet').value = walletId;
                // Remove the current wallet from the "to wallet" options
                const toWalletSelect = document.getElementById('to_wallet');
                for (let option of toWalletSelect.options) {
                    option.disabled = option.value === walletId;
                }
                showModal('transferModal');
            }

            function editWallet(wallet) {
                const editForm = document.getElementById('editWalletForm');
                editForm.action = `/wallet/update/${wallet.id}`;
                document.getElementById('edit_name').value = wallet.name;
                document.getElementById('edit_type').value = wallet.type;
                showModal('editWalletModal');
            }

            function deleteWallet() {
                if (confirm('Are you sure you want to delete this wallet?')) {
                    const form = document.getElementById('editWalletForm');
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'action';
                    input.value = 'delete';
                    form.appendChild(input);
                    form.submit();
                }
            }

            // Make wallet cards clickable
            document.addEventListener('DOMContentLoaded', function() {
                const wallets = {{ wallets_list | tojson }};
                document.querySelectorAll('.wallet-card').forEach((card, index) => {
                    card.addEventListener('click', () => editWallet(wallets[index]));
                });
            });
        </script>
    </body>
    </html>
    ''', wallets=user_wallets, wallets_list=wallets_list)

@app.route('/budgets')
@login_required
def budgets():
    # Get budgets by category
    income_budgets = Budget.query.filter_by(category='Income').all()
    savings_budgets = Budget.query.filter_by(category='Savings').all()
    expense_budgets = Budget.query.filter_by(category='Expenses').all()
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Budgets - Know Your $avings</title>
        <style>
            :root {
                --primary-color: #FFD700;
                --primary-dark: #FFC700;
                --accent-color: #FFB700;
                --header-bg: #0A1929;
                --bg-dark: #000000;
                --bg-lighter: #1A2027;
                --text-light: #ffffff;
                --text-muted: #94A3B8;
                --card-bg: #0A1929;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 0;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: var(--bg-dark);
                color: var(--text-light);
                line-height: 1.6;
            }
            
            ''' + LOGGED_IN_HEADER_STYLE + '''

            .budgets-content {
                padding: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }

            .welcome-header {
                margin-bottom: 2rem;
            }

            .welcome-title {
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }

            .welcome-subtitle {
                color: var(--text-muted);
            }

            .header-actions {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 2rem;
            }

            .budget-section {
                margin-bottom: 2rem;
            }
            
            .section-title {
                font-size: 1.5rem;
                color: var(--text-light);
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }

            .budgets-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }

            .budget-card {
                background: var(--header-bg);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                cursor: pointer;
                transition: transform 0.2s ease;
            }

            .budget-card:hover {
                transform: translateY(-2px);
            }

            .budget-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }

            .budget-name {
                font-size: 1.2rem;
                font-weight: 600;
            }

            .budget-period {
                color: var(--text-muted);
                font-size: 0.9rem;
            }

            .budget-amount {
                font-size: 2rem;
                font-weight: 600;
                margin: 1rem 0;
            }

            .budget-progress {
                background: rgba(255, 255, 255, 0.1);
                height: 8px;
                border-radius: 4px;
                margin: 1rem 0;
                overflow: hidden;
            }

            .progress-bar {
                height: 100%;
                background: var(--primary-color);
                transition: width 0.3s ease;
            }

            .budget-details {
                display: flex;
                justify-content: space-between;
                color: var(--text-muted);
                font-size: 0.9rem;
            }

            .action-button {
                padding: 0.5rem 1rem;
                border: none;
                border-radius: 8px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 0.95rem;
            }

            .primary-button {
                background: var(--primary-color);
                color: #000000;
                font-weight: 600;
            }

            .secondary-button {
                background: rgba(255, 255, 255, 0.1);
                color: var(--text-light);
                font-weight: 500;
            }

            .action-button:hover {
                transform: translateY(-2px);
            }

            /* Modal styles */
            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                z-index: 1001;
            }

            .modal-content {
                background: var(--header-bg);
                padding: 2rem;
                border-radius: 15px;
                width: 90%;
                max-width: 500px;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            .modal-title {
                margin-bottom: 1.5rem;
                font-size: 1.5rem;
            }

            .form-group {
                margin-bottom: 1rem;
            }

            .form-group label {
                display: block;
                margin-bottom: 0.5rem;
                color: var(--text-muted);
            }

            .form-group input, .form-group select {
                width: 100%;
                padding: 0.5rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.05);
                color: var(--text-light);
                font-family: inherit;
            }

            .modal-actions {
                display: flex;
                justify-content: flex-end;
                gap: 1rem;
                margin-top: 1.5rem;
            }

            .close-button {
                position: absolute;
                right: 1rem;
                top: 1rem;
                background: none;
                border: none;
                color: var(--text-muted);
                cursor: pointer;
                font-size: 1.5rem;
            }
        </style>
    </head>
    <body>
        ''' + LOGGED_IN_HEADER + '''
        <div class="content-wrapper">
            <div class="budgets-content">
                <div class="welcome-header">
                    <h1 class="welcome-title">Your Budgets</h1>
                    <p class="welcome-subtitle">Track and manage your spending limits</p>
                </div>

                <div class="header-actions">
                    <button class="action-button primary-button" onclick="showNewBudgetModal()">Add New Budget</button>
                </div>

                <!-- Income Section -->
                <div class="budget-section">
                    <h2 class="section-title">Income</h2>
                    <div class="budgets-grid">
                        {% for budget in income_budgets %}
                        <div class="budget-card" onclick="editBudget({
                            id: {{ budget.id }},
                            name: '{{ budget.name|safe }}',
                            amount: {{ budget.amount }},
                            period: '{{ budget.period }}',
                            category: '{{ budget.category }}'
                        })">
                            <div class="budget-header">
                                <div>
                                    <h3 class="budget-name">{{ budget.name }}</h3>
                                    <span class="budget-period">{{ budget.period }}</span>
                                </div>
                            </div>
                            <div class="budget-amount">${{ "%.2f"|format(budget.amount) }}</div>
                            <div class="budget-progress">
                                <div class="progress-bar" style="width: {{ (budget.current_amount / budget.amount * 100) if budget.amount > 0 else 0 }}%"></div>
                            </div>
                            <div class="budget-details">
                                <span>Current: ${{ "%.2f"|format(budget.current_amount) }}</span>
                                <span>Target: ${{ "%.2f"|format(budget.amount) }}</span>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>

                <!-- Savings Section -->
                <div class="budget-section">
                    <h2 class="section-title">Savings</h2>
                    <div class="budgets-grid">
                        {% for budget in savings_budgets %}
                        <div class="budget-card" onclick="editBudget({
                            id: {{ budget.id }},
                            name: '{{ budget.name|safe }}',
                            amount: {{ budget.amount }},
                            period: '{{ budget.period }}',
                            category: '{{ budget.category }}'
                        })">
                            <div class="budget-header">
                                <div>
                                    <h3 class="budget-name">{{ budget.name }}</h3>
                                    <span class="budget-period">{{ budget.period }}</span>
                                </div>
                            </div>
                            <div class="budget-amount">${{ "%.2f"|format(budget.amount) }}</div>
                            <div class="budget-progress">
                                <div class="progress-bar" style="width: {{ (budget.current_amount / budget.amount * 100) if budget.amount > 0 else 0 }}%"></div>
                            </div>
                            <div class="budget-details">
                                <span>Current: ${{ "%.2f"|format(budget.current_amount) }}</span>
                                <span>Target: ${{ "%.2f"|format(budget.amount) }}</span>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>

                <!-- Expenses Section -->
                <div class="budget-section">
                    <h2 class="section-title">Expenses</h2>
                    <div class="budgets-grid">
                        {% for budget in expense_budgets %}
                        <div class="budget-card" onclick="editBudget({
                            id: {{ budget.id }},
                            name: '{{ budget.name|safe }}',
                            amount: {{ budget.amount }},
                            period: '{{ budget.period }}',
                            category: '{{ budget.category }}'
                        })">
                            <div class="budget-header">
                                <div>
                                    <h3 class="budget-name">{{ budget.name }}</h3>
                                    <span class="budget-period">{{ budget.period }}</span>
                                </div>
                            </div>
                            <div class="budget-amount">${{ "%.2f"|format(budget.amount) }}</div>
                            <div class="budget-progress">
                                <div class="progress-bar" style="width: {{ (budget.current_amount / budget.amount * 100) if budget.amount > 0 else 0 }}%"></div>
                            </div>
                            <div class="budget-details">
                                <span>Current: ${{ "%.2f"|format(budget.current_amount) }}</span>
                                <span>Target: ${{ "%.2f"|format(budget.amount) }}</span>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>

        <!-- New Budget Modal -->
        <div id="newBudgetModal" class="modal">
            <div class="modal-content">
                <button class="close-button" onclick="closeModal('newBudgetModal')">&times;</button>
                <h2 class="modal-title">Add New Budget</h2>
                <form action="{{ url_for('add_budget') }}" method="POST">
                    <div class="form-group">
                        <label for="name">Budget Name</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="amount">Amount</label>
                        <input type="number" id="amount" name="amount" step="0.01" required>
                    </div>
                    <div class="form-group">
                        <label for="category">Category</label>
                        <select id="category" name="category" required>
                            <option value="Income">Income</option>
                            <option value="Savings">Savings</option>
                            <option value="Expenses">Expenses</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="period">Period</label>
                        <select id="period" name="period" required>
                            <option value="Monthly">Monthly</option>
                            <option value="Weekly">Weekly</option>
                            <option value="Yearly">Yearly</option>
                        </select>
                    </div>
                    <div class="modal-actions">
                        <button type="button" class="action-button secondary-button" onclick="closeModal('newBudgetModal')">Cancel</button>
                        <button type="submit" class="action-button primary-button">Add Budget</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Edit Budget Modal -->
        <div id="editBudgetModal" class="modal">
            <div class="modal-content">
                <button class="close-button" onclick="closeModal('editBudgetModal')">&times;</button>
                <h2 class="modal-title">Edit Budget</h2>
                <form action="" method="POST" id="editBudgetForm">
                    <div class="form-group">
                        <label for="edit_name">Budget Name</label>
                        <input type="text" id="edit_name" name="name" required>
                    </div>
                    <div class="form-group">
                        <label for="edit_amount">Amount</label>
                        <input type="number" id="edit_amount" name="amount" step="0.01" required>
                    </div>
                    <div class="form-group">
                        <label for="edit_period">Period</label>
                        <select id="edit_period" name="period" required>
                            <option value="Monthly">Monthly</option>
                            <option value="Weekly">Weekly</option>
                            <option value="Yearly">Yearly</option>
                        </select>
                    </div>
                    <div class="modal-actions">
                        <button type="button" class="action-button secondary-button" onclick="deleteBudget()">Delete</button>
                        <button type="submit" class="action-button primary-button">Update</button>
                    </div>
                </form>
            </div>
        </div>

        <script>
            function showModal(modalId) {
                document.getElementById(modalId).style.display = 'block';
            }

            function closeModal(modalId) {
                document.getElementById(modalId).style.display = 'none';
            }

            function showNewBudgetModal() {
                showModal('newBudgetModal');
            }

            function editBudget(budget) {
                const editForm = document.getElementById('editBudgetForm');
                editForm.action = `/budget/update/${budget.id}`;
                document.getElementById('edit_name').value = budget.name;
                document.getElementById('edit_amount').value = budget.amount;
                document.getElementById('edit_period').value = budget.period;
                showModal('editBudgetModal');
            }

            function deleteBudget() {
                if (confirm('Are you sure you want to delete this budget?')) {
                    const form = document.getElementById('editBudgetForm');
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'action';
                    input.value = 'delete';
                    form.appendChild(input);
                    form.submit();
                }
            }

            // Close modals when clicking outside
            window.onclick = function(event) {
                if (event.target.classList.contains('modal')) {
                    event.target.style.display = 'none';
                }
            }
        </script>
    </body>
    </html>
    ''', 
    income_budgets=income_budgets,
    savings_budgets=savings_budgets,
    expense_budgets=expense_budgets)

@app.route('/budget/add', methods=['POST'])
@login_required
def add_budget():
    category = request.form.get('category')
    name = request.form.get('name')
    amount = float(request.form.get('amount'))
    period = request.form.get('period')
    
    new_budget = Budget(
        category=category,
        name=name,
        amount=amount,
        period=period
    )
    
    db.session.add(new_budget)
    db.session.commit()
    
    flash(f'New {category.lower()} budget added successfully!', 'success')
    return redirect(url_for('budgets'))

@app.route('/reports')
@login_required
def reports():
    # Calculate monthly totals from Budgets (not Transactions)
    monthly_income = db.session.query(
        func.sum(Budget.amount)
    ).filter(Budget.category == 'Income').scalar() or 0.0
    
    monthly_expenses = db.session.query(
        func.sum(Budget.amount)
    ).filter(Budget.category == 'Expenses').scalar() or 0.0
    
    # No need to negate expenses as they're stored as positive values
    monthly_expenses_display = monthly_expenses
    
    # Create spending by category data - include all categories
    category_totals = []
    
    # Add Income total
    income_total = db.session.query(
        func.sum(Budget.amount)
    ).filter(Budget.category == 'Income').scalar() or 0.0
    if income_total > 0:
        category_totals.append(('Income', income_total))
    
    # Add Savings total
    savings_total = db.session.query(
        func.sum(Budget.amount)
    ).filter(Budget.category == 'Savings').scalar() or 0.0
    if savings_total > 0:
        category_totals.append(('Savings', savings_total))
    
    # Add Expenses total
    expenses_total = db.session.query(
        func.sum(Budget.amount)
    ).filter(Budget.category == 'Expenses').scalar() or 0.0
    if expenses_total > 0:
        category_totals.append(('Expenses', expenses_total))
    
    # Debug print
    print("Monthly Expenses:", monthly_expenses)
    print("Category Totals:", category_totals)
    
    # Prepare data for charts
    categories = [cat for cat, _ in category_totals]
    amounts = [float(amt) for _, amt in category_totals]
    
    # Get transaction history data
    transactions_by_date = db.session.query(
        Transaction.date,
        func.sum(Transaction.amount)
    ).group_by(Transaction.date).order_by(Transaction.date).all()
    
    # Format dates and amounts
    dates = []
    transaction_amounts = []
    for date, amount in transactions_by_date:
        if isinstance(date, str):
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                dates.append(date_obj.strftime('%Y-%m-%d'))
            except ValueError:
                continue
        else:
            dates.append(date.strftime('%Y-%m-%d'))
        transaction_amounts.append(float(amount))

    # Calculate net savings (Income - Expenses)
    net_savings = monthly_income - monthly_expenses

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reports - Know Your $avings</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            :root {
                --primary-color: #FFD700;
                --primary-dark: #FFC700;
                --accent-color: #FFB700;
                --header-bg: #0A1929;
                --bg-dark: #000000;
                --bg-lighter: #1A2027;
                --text-light: #ffffff;
                --text-muted: #94A3B8;
                --card-bg: #0A1929;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 0;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: var(--bg-dark);
                color: var(--text-light);
                line-height: 1.6;
            }
            
            ''' + LOGGED_IN_HEADER_STYLE + '''

            .reports-content {
                padding: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }

            .welcome-header {
                margin-bottom: 2rem;
            }

            .welcome-title {
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }

            .welcome-subtitle {
                color: var(--text-muted);
            }

            .reports-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }

            .report-card {
                background: var(--header-bg);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            .report-title {
                font-size: 1.1rem;
                color: var(--text-muted);
                margin-bottom: 1rem;
            }

            .report-amount {
                font-size: 2rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
            }

            .chart-container {
                background: var(--header-bg);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 1.5rem;
            }

            .chart-title {
                font-size: 1.1rem;
                color: var(--text-muted);
                margin-bottom: 1rem;
            }
        </style>
    </head>
    <body>
        ''' + LOGGED_IN_HEADER + '''
        <div class="content-wrapper">
            <div class="reports-content">
                <div class="welcome-header">
                    <h1 class="welcome-title">Financial Reports</h1>
                    <p class="welcome-subtitle">View your financial analytics and trends</p>
                </div>

                <div class="reports-grid">
                    <div class="report-card">
                        <h2 class="report-title">Monthly Income</h2>
                        <div class="report-amount">${{ "%.2f"|format(monthly_income) }}</div>
                    </div>

                    <div class="report-card">
                        <h2 class="report-title">Monthly Expenses</h2>
                        <div class="report-amount">${{ "%.2f"|format(monthly_expenses_display) }}</div>
                    </div>

                    <div class="report-card">
                        <h2 class="report-title">Net Savings</h2>
                        <div class="report-amount">${{ "%.2f"|format(net_savings) }}</div>
                    </div>
                </div>

                <div class="chart-container">
                    <h2 class="chart-title">Spending by Category</h2>
                    <div id="categoryChart"></div>
                </div>

                <div class="chart-container">
                    <h2 class="chart-title">Monthly Transaction History</h2>
                    <div id="transactionChart"></div>
                </div>
            </div>
        </div>

        <script>
            // Spending by Category Bar Chart
            const categoryData = {
                x: {{ categories|tojson }},
                y: {{ amounts|tojson }},
                type: 'bar',
                marker: {
                    color: ['#4CAF50', '#FFD700', '#FF6B6B'],  // Green for income, Gold for savings, Red for expenses
                    borderradius: 4    // Rounded corners for bars
                },
                hoverinfo: 'y',
                hoverlabel: {
                    bgcolor: '#0A1929',
                    bordercolor: '#0A1929',
                    font: { 
                        family: 'Inter',
                        color: '#ffffff' 
                    }
                }
            };

            const categoryLayout = {
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                height: 400,
                font: {
                    family: 'Inter',
                    color: '#94A3B8',
                    size: 12
                },
                showlegend: false,
                xaxis: {
                    showgrid: false,
                    title: {
                        text: 'Categories',
                        font: {
                            family: 'Inter',
                            size: 12,
                            color: '#94A3B8'
                        }
                    },
                    tickfont: {
                        family: 'Inter',
                        size: 12
                    },
                    fixedrange: true  // Disable zoom/pan
                },
                yaxis: {
                    showgrid: true,
                    gridcolor: 'rgba(255,255,255,0.1)',
                    title: {
                        text: 'Amount ($)',
                        font: {
                            family: 'Inter',
                            size: 12,
                            color: '#94A3B8'
                        }
                    },
                    tickprefix: '$',
                    tickfont: {
                        family: 'Inter',
                        size: 12,
                        color: '#94A3B8'
                    },
                    tickformat: ',.0f',  // Remove decimal places
                    fixedrange: true  // Disable zoom/pan
                },
                margin: {
                    l: 60,
                    r: 20,
                    t: 20,
                    b: 40
                },
                bargap: 0.4,  // Increased gap between bars
                shapes: [{  // Add rounded corners to the plot area
                    type: 'rect',
                    xref: 'paper',
                    yref: 'paper',
                    x0: 0,
                    y0: 0,
                    x1: 1,
                    y1: 1,
                    line: {
                        width: 0
                    },
                    layer: 'below'
                }],
                dragmode: false  // Disable dragging
            };

            const config = {
                displayModeBar: false,
                responsive: true,
                staticPlot: true  // Make plot completely static
            };

            Plotly.newPlot('categoryChart', [categoryData], categoryLayout, config);

            // Transaction History Line Chart
            const transactionData = {
                x: {{ dates|tojson|safe }},
                y: {{ transaction_amounts|tojson|safe }},
                type: 'scatter',
                mode: 'lines+markers',
                line: {
                    color: '#FFD700',
                    width: 2
                },
                marker: {
                    color: '#FFD700',
                    size: 6
                },
                hoverinfo: 'y',
                hoverlabel: {
                    bgcolor: '#0A1929',
                    bordercolor: '#0A1929',
                    font: { color: '#ffffff' }
                }
            };

            const transactionLayout = {
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                height: 400,
                font: {
                    color: '#94A3B8',
                    family: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif'
                },
                xaxis: {
                    showgrid: true,
                    gridcolor: 'rgba(255,255,255,0.1)',
                    tickfont: {
                        color: '#94A3B8'
                    }
                },
                yaxis: {
                    showgrid: true,
                    gridcolor: 'rgba(255,255,255,0.1)',
                    tickprefix: '$',
                    tickfont: {
                        color: '#94A3B8'
                    }
                },
                margin: {
                    l: 50,
                    r: 20,
                    t: 20,
                    b: 50
                },
                dragmode: false
            };

            Plotly.newPlot('transactionChart', [transactionData], transactionLayout, config);
        </script>
    </body>
    </html>
    ''', 
    monthly_income=monthly_income,
    monthly_expenses=monthly_expenses,
    monthly_expenses_display=monthly_expenses_display,
    net_savings=net_savings,  # Add this to the template variables
    categories=categories,
    amounts=amounts,
    dates=dates,
    transaction_amounts=transaction_amounts)

@app.route('/settings')
@login_required
def settings():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Settings - Know Your $avings</title>
        <style>
            :root {
                --primary-color: #FFD700;
                --primary-dark: #FFC700;
                --accent-color: #FFB700;
                --header-bg: #0A1929;
                --bg-dark: #000000;
                --bg-lighter: #1A2027;
                --text-light: #ffffff;
                --text-muted: #94A3B8;
                --card-bg: #0A1929;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                margin: 0;
                padding: 0;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: var(--bg-dark);
                color: var(--text-light);
                line-height: 1.6;
            }
            
            ''' + LOGGED_IN_HEADER_STYLE + '''

            .settings-content {
                padding: 20px;
                max-width: 800px;
                margin: 0 auto;
            }

            .welcome-header {
                margin-bottom: 2rem;
            }

            .welcome-title {
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }

            .welcome-subtitle {
                color: var(--text-muted);
            }

            .settings-section {
                background: var(--header-bg);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 1.5rem;
            }

            .section-title {
                font-size: 1.2rem;
                color: var(--text-light);
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }

            .settings-form {
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }

            .form-group {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }

            .form-group label {
                color: var(--text-muted);
                font-size: 0.9rem;
            }

            .form-group input,
            .form-group select {
                padding: 0.5rem;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                background: rgba(255, 255, 255, 0.05);
                color: var(--text-light);
                font-family: inherit;
            }

            .action-button {
                padding: 0.5rem 1rem;
                border: none;
                border-radius: 8px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                font-family: inherit;
            }

            .primary-button {
                background: var(--primary-color);
                color: #000000;
            }

            .danger-button {
                background: #FF4444;
                color: white;
            }

            .action-button:hover {
                transform: translateY(-2px);
            }

            .settings-footer {
                margin-top: 2rem;
                padding-top: 1rem;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center;
                color: var(--text-muted);
                font-size: 0.9rem;
            }
        </style>
    </head>
    <body>
        ''' + LOGGED_IN_HEADER + '''
        <div class="content-wrapper">
            <div class="settings-content">
                <div class="welcome-header">
                    <h1 class="welcome-title">Settings</h1>
                    <p class="welcome-subtitle">Manage your account preferences</p>
                </div>

                <!-- Account Settings -->
                <div class="settings-section">
                    <h2 class="section-title">Account Settings</h2>
                    <form class="settings-form" action="{{ url_for('update_account') }}" method="POST">
                        <div class="form-group">
                            <label for="email">Email Address</label>
                            <input type="email" id="email" name="email" value="{{ current_user.email }}" required>
                        </div>
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input type="text" id="username" name="username" value="{{ current_user.username }}" required>
                        </div>
                        <button type="submit" class="action-button primary-button">Update Account</button>
                    </form>
                </div>

                <!-- Password Change -->
                <div class="settings-section">
                    <h2 class="section-title">Change Password</h2>
                    <form class="settings-form" action="{{ url_for('change_password') }}" method="POST">
                        <div class="form-group">
                            <label for="current_password">Current Password</label>
                            <input type="password" id="current_password" name="current_password" required>
                        </div>
                        <div class="form-group">
                            <label for="new_password">New Password</label>
                            <input type="password" id="new_password" name="new_password" required>
                        </div>
                        <div class="form-group">
                            <label for="confirm_password">Confirm New Password</label>
                            <input type="password" id="confirm_password" name="confirm_password" required>
                        </div>
                        <button type="submit" class="action-button primary-button">Change Password</button>
                    </form>
                </div>

                <!-- Delete Account -->
                <div class="settings-section">
                    <h2 class="section-title">Delete Account</h2>
                    <form class="settings-form" action="{{ url_for('delete_account') }}" method="POST" 
                          onsubmit="return confirm('Are you sure you want to delete your account? This action cannot be undone.')">
                        <p style="color: var(--text-muted); margin-bottom: 1rem;">
                            Warning: This action is permanent and cannot be undone. All your data will be deleted.
                        </p>
                        <button type="submit" class="action-button danger-button">Delete Account</button>
                    </form>
                </div>

                <div class="settings-footer">
                    <p>Know Your $avings &copy; 2024</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', current_user=current_user)  # Pass current_user to the template

# Add the necessary routes for handling settings actions
@app.route('/update_account', methods=['POST'])
@login_required
def update_account():
    email = request.form.get('email')
    username = request.form.get('username')
    
    # Validate email and username
    if not email or not username:
        flash('Email and username are required.', 'error')
        return redirect(url_for('settings'))
    
    # Check if email is already taken by another user
    existing_user = User.query.filter(User.email == email, User.id != current_user.id).first()
    if existing_user:
        flash('Email address is already in use.', 'error')
        return redirect(url_for('settings'))
    
    # Update user information
    current_user.email = email
    current_user.username = username
    db.session.commit()
    
    flash('Account settings updated successfully!', 'success')
    return redirect(url_for('settings'))

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Verify current password
    if not current_user.check_password(current_password):
        flash('Current password is incorrect.', 'error')
        return redirect(url_for('settings'))
    
    # Validate new password
    if new_password != confirm_password:
        flash('New passwords do not match.', 'error')
        return redirect(url_for('settings'))
    
    # Update password
    current_user.set_password(new_password)
    db.session.commit()
    
    flash('Password changed successfully!', 'success')
    return redirect(url_for('settings'))

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    # Delete user's data
    Transaction.query.filter_by(user_id=current_user.id).delete()
    Budget.query.filter_by(user_id=current_user.id).delete()
    
    # Delete user
    db.session.delete(current_user)
    db.session.commit()
    
    logout_user()
    flash('Your account has been deleted successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/features')
def features():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Features - FinanceTracker</title>
        <style>
            :root {
                --primary-color: #FFD700;
                --primary-dark: #FFC700;
                --accent-color: #FFB700;
                --header-bg: #0A1929;
                --bg-dark: #000000;
                --bg-darker: #000000;
                --bg-lighter: #111111;
                --text-light: #ffffff;
                --text-muted: #94A3B8;
                --card-bg: #0A1929;
                --success-color: #4CAF50;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                background-color: var(--bg-dark);
                color: var(--text-light);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                line-height: 1.6;
            }
            
            header {
                background-color: var(--header-bg);
                backdrop-filter: blur(10px);
                padding: 1.2rem;
                position: fixed;
                width: 100%;
                top: 0;
                z-index: 1000;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            nav {
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 1rem;
            }
            
            .logo {
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--text-light);
                text-decoration: none;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .logo span {
                color: var(--primary-color);
            }
            
            .nav-links {
                display: flex;
                gap: 2rem;
                align-items: center;
            }
            
            .nav-links a {
                color: var(--text-light);
                text-decoration: none;
                font-weight: 500;
                font-size: 0.95rem;
                transition: all 0.3s ease;
                padding: 0.5rem 1rem;
                border-radius: 8px;
            }
            
            .nav-links a:hover {
                color: var(--primary-color);
                background: rgba(255, 215, 0, 0.1);
            }
            
            .nav-links a.login {
                background: var(--primary-color);
                color: #000000;
                font-weight: 600;
            }
            
            .nav-links a.login:hover {
                background: var(--primary-dark);
                opacity: 0.9;
            }

            .nav-links a.signup {
                background: transparent;
                color: var(--primary-color);
                font-weight: 600;
                border: 2px solid var(--primary-color);
            }
            
            .nav-links a.signup:hover {
                background: rgba(255, 215, 0, 0.1);
                color: var(--primary-color);
            }

            .features-section {
                padding: 140px 20px 60px;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .feature-category {
                margin-bottom: 80px;
            }
            
            .category-title {
                font-size: 2.5rem;
                margin-bottom: 2rem;
                color: var(--primary-color);
            }
            
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 2rem;
            }
            
            .feature-item {
                background: var(--header-bg);
                padding: 2rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: transform 0.3s ease;
            }
            
            .feature-item:hover {
                transform: translateY(-5px);
            }
            
            .feature-icon {
                font-size: 2rem;
                margin-bottom: 1rem;
                color: var(--primary-color);
            }
            
            .feature-name {
                font-size: 1.5rem;
                margin-bottom: 1rem;
                color: var(--text-light);
            }
            
            .feature-desc {
                color: var(--text-muted);
                line-height: 1.6;
            }
            
            .feature-details {
                margin-top: 1rem;
                padding-top: 1rem;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .feature-details ul {
                list-style: none;
            }
            
            .feature-details li {
                color: var(--text-muted);
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .feature-details li::before {
                content: "✓";
                color: var(--primary-color);
            }
        </style>
    </head>
    <body>
        <header>
            <nav>
                <a href="/" class="logo">Know Your <span>$avings</span></a>
                <div class="nav-links">
                    <a href="/">Home</a>
                    <a href="/features">Features</a>
                    <a href="/pricing">Pricing</a>
                    <a href="/login" class="login">Login</a>
                </div>
            </nav>
        </header>

        <div class="features-section">
            <div class="feature-category">
                <h2 class="category-title">Financial Tracking</h2>
                <div class="feature-grid">
                    <div class="feature-item">
                        <div class="feature-icon">📊</div>
                        <h3 class="feature-name">Smart Analytics</h3>
                        <p class="feature-desc">Advanced expense tracking with intelligent categorization</p>
                        <div class="feature-details">
                            <ul>
                                <li>Smart transaction categorization</li>
                                <li>Custom categories and tags</li>
                                <li>Receipt scanning and storage</li>
                                <li>Pattern recognition analysis</li>
                            </ul>
                        </div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">💰</div>
                        <h3 class="feature-name">Multi-Currency Support</h3>
                        <p class="feature-desc">Handle transactions in multiple currencies with real-time conversion</p>
                        <div class="feature-details">
                            <ul>
                                <li>Real-time exchange rates</li>
                                <li>Automatic currency conversion</li>
                                <li>Multi-currency reports</li>
                                <li>Currency gain/loss tracking</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <div class="feature-category">
                <h2 class="category-title">Budgeting Tools</h2>
                <div class="feature-grid">
                    <div class="feature-item">
                        <div class="feature-icon">🎯</div>
                        <h3 class="feature-name">Smart Budgets</h3>
                        <p class="feature-desc">AI-powered budget recommendations based on your spending habits</p>
                        <div class="feature-details">
                            <ul>
                                <li>Personalized budget suggestions</li>
                                <li>Category-specific budgets</li>
                                <li>Flexible budget periods</li>
                                <li>Real-time budget tracking</li>
                            </ul>
                        </div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">💸</div>
                        <h3 class="feature-name">Bill Tracking</h3>
                        <p class="feature-desc">Never miss a payment with automated bill tracking and reminders</p>
                        <div class="feature-details">
                            <ul>
                                <li>Bill due date reminders</li>
                                <li>Recurring bill setup</li>
                                <li>Payment confirmation</li>
                                <li>Bill history and analytics</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <div class="feature-category">
                <h2 class="category-title">Reports & Insights</h2>
                <div class="feature-grid">
                    <div class="feature-item">
                        <div class="feature-icon">📈</div>
                        <h3 class="feature-name">Advanced Analytics</h3>
                        <p class="feature-desc">Detailed financial reports with predictive insights</p>
                        <div class="feature-details">
                            <ul>
                                <li>Custom report generation</li>
                                <li>Trend analysis</li>
                                <li>Spending forecasts</li>
                                <li>Investment tracking</li>
                            </ul>
                        </div>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">🎯</div>
                        <h3 class="feature-name">Smart Insights</h3>
                        <p class="feature-desc">Get personalized financial recommendations based on your habits</p>
                        <div class="feature-details">
                            <ul>
                                <li>Spending optimization suggestions</li>
                                <li>Smart savings opportunities</li>
                                <li>Investment recommendations</li>
                                <li>Predictive analysis</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/pricing')
def pricing():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Pricing - FinanceTracker</title>
        <style>
            :root {
                --primary-color: #FFD700;
                --primary-dark: #FFC700;
                --accent-color: #FFB700;
                --header-bg: #0A1929;
                --bg-dark: #000000;
                --bg-darker: #000000;
                --bg-lighter: #111111;
                --text-light: #ffffff;
                --text-muted: #94A3B8;
                --card-bg: #0A1929;
                --success-color: #4CAF50;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                background-color: var(--bg-dark);
                color: var(--text-light);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                line-height: 1.6;
            }
            
            header {
                background-color: var(--header-bg);
                backdrop-filter: blur(10px);
                padding: 1.2rem;
                position: fixed;
                width: 100%;
                top: 0;
                z-index: 1000;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            nav {
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 1rem;
            }
            
            .logo {
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--text-light);
                text-decoration: none;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .logo span {
                color: var(--primary-color);
            }
            
            .nav-links {
                display: flex;
                gap: 2rem;
                align-items: center;
            }
            
            .nav-links a {
                color: var(--text-light);
                text-decoration: none;
                font-weight: 500;
                font-size: 0.95rem;
                transition: all 0.3s ease;
                padding: 0.5rem 1rem;
                border-radius: 8px;
            }
            
            .nav-links a:hover {
                color: var(--primary-color);
                background: rgba(255, 215, 0, 0.1);
            }
            
            .nav-links a.login {
                background: var(--primary-color);
                color: #000000;
                font-weight: 600;
            }
            
            .nav-links a.login:hover {
                background: var(--primary-dark);
                opacity: 0.9;
            }

            .nav-links a.signup {
                background: transparent;
                color: var(--primary-color);
                font-weight: 600;
                border: 2px solid var(--primary-color);
            }
            
            .nav-links a.signup:hover {
                background: rgba(255, 215, 0, 0.1);
                color: var(--primary-color);
            }

            .pricing-section {
                padding: 140px 20px 60px;
                max-width: 1200px;
                margin: 0 auto;
            }

            .pricing-header {
                text-align: center;
                margin-bottom: 60px;
            }

            .pricing-title {
                font-size: 3rem;
                margin-bottom: 1rem;
                background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .pricing-subtitle {
                color: var(--text-muted);
                font-size: 1.2rem;
                max-width: 600px;
                margin: 0 auto;
            }

            .pricing-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                padding: 2rem 0;
            }

            .pricing-card {
                background: var(--header-bg);
                border-radius: 15px;
                padding: 2rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: transform 0.3s ease;
                display: flex;
                flex-direction: column;
            }

            .pricing-card:hover {
                transform: translateY(-5px);
            }

            .pricing-card.popular {
                border: 2px solid var(--primary-color);
                position: relative;
            }

            .popular-badge {
                position: absolute;
                top: -12px;
                left: 50%;
                transform: translateX(-50%);
                background: var(--primary-color);
                color: #000000;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 600;
            }

            .plan-name {
                font-size: 1.5rem;
                margin-bottom: 1rem;
                color: var(--text-light);
            }

            .plan-price {
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 1.5rem;
                color: var(--primary-color);
            }

            .plan-price span {
                font-size: 1rem;
                color: var(--text-muted);
            }

            .plan-features {
                list-style: none;
                margin-bottom: 2rem;
                flex-grow: 1;
            }

            .plan-features li {
                color: var(--text-muted);
                margin-bottom: 0.8rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .plan-features li::before {
                content: "✓";
                color: var(--primary-color);
            }

            .plan-button {
                display: inline-block;
                padding: 1rem 2rem;
                background: var(--primary-color);
                color: #000000;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 600;
                text-align: center;
                transition: all 0.3s ease;
            }

            .plan-button:hover {
                background: var(--primary-dark);
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <header>
            <nav>
                <a href="/" class="logo">Know Your <span>$avings</span></a>
                <div class="nav-links">
                    <a href="/">Home</a>
                    <a href="/features">Features</a>
                    <a href="/pricing">Pricing</a>
                    <a href="/login" class="login">Login</a>
                </div>
            </nav>
        </header>

        <div class="pricing-section">
            <div class="pricing-header">
                <h1 class="pricing-title">Simple, Transparent Pricing</h1>
                <p class="pricing-subtitle">Choose the plan that best fits your needs</p>
            </div>
            
            <div class="pricing-grid">
                <div class="pricing-card">
                    <h2 class="plan-name">Free</h2>
                    <div class="plan-price">$0<span>/month</span></div>
                    <ul class="plan-features">
                        <li>Basic expense tracking</li>
                        <li>Monthly budget planning</li>
                        <li>Basic reports</li>
                        <li>Responsive web access</li>
                        <li>Up to 2 accounts</li>
                    </ul>
                    <a href="/signup" class="plan-button">Get Started</a>
                </div>

                <div class="pricing-card popular">
                    <div class="popular-badge">Most Popular</div>
                    <h2 class="plan-name">Premium</h2>
                    <div class="plan-price">$9.99<span>/month</span></div>
                    <ul class="plan-features">
                        <li>Everything in Free</li>
                        <li>Smart financial insights</li>
                        <li>Advanced analytics</li>
                        <li>Custom categories</li>
                        <li>Unlimited accounts</li>
                        <li>Bill reminders</li>
                        <li>Investment tracking</li>
                    </ul>
                    <a href="/signup" class="plan-button">Start Free Trial</a>
                </div>

                <div class="pricing-card">
                    <h2 class="plan-name">Business</h2>
                    <div class="plan-price">$29.99<span>/month</span></div>
                    <ul class="plan-features">
                        <li>Everything in Premium</li>
                        <li>API access</li>
                        <li>Team collaboration</li>
                        <li>Custom reporting</li>
                        <li>Priority support</li>
                        <li>Audit logs</li>
                        <li>Data export</li>
                        <li>SSO integration</li>
                    </ul>
                    <a href="/signup" class="plan-button">Contact Sales</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']  # Changed from email to username
        password = request.form['password']
        
        # Simple admin authentication
        if username == 'admin' and password == 'admin':
            session['user_id'] = 1
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Login - FinanceTracker</title>
        <style>
            :root {
                --primary-color: #FFD700;
                --primary-dark: #FFC700;
                --accent-color: #FFB700;
                --header-bg: #0A1929;
                --bg-dark: #000000;
                --bg-darker: #000000;
                --bg-lighter: #111111;
                --text-light: #ffffff;
                --text-muted: #94A3B8;
                --card-bg: #0A1929;
                --success-color: #4CAF50;
                --error-color: #FF4444;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                background-color: var(--bg-dark);
                color: var(--text-light);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                line-height: 1.6;
            }
            
            header {
                background-color: var(--header-bg);
                backdrop-filter: blur(10px);
                padding: 1.2rem;
                position: fixed;
                width: 100%;
                top: 0;
                z-index: 1000;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            nav {
                display: flex;
                justify-content: space-between;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 1rem;
            }
            
            .logo {
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--text-light);
                text-decoration: none;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .logo span {
                color: var(--primary-color);
            }
            
            .nav-links {
                display: flex;
                gap: 2rem;
                align-items: center;
            }
            
            
            .nav-links a {
                color: var(--text-light);
                text-decoration: none;
                font-weight: 500;
                font-size: 0.95rem;
                transition: all 0.3s ease;
                padding: 0.5rem 1rem;
                border-radius: 8px;
            }
            
            .nav-links a:hover {
                color: var(--primary-color);
                background: rgba(255, 215, 0, 0.1);
            }
            
            .nav-links a.login {
                background: var(--primary-color);
                color: #000000;
                font-weight: 600;
            }
            
            .nav-links a.login:hover {
                background: var(--primary-dark);
                opacity: 0.9;
            }

            .nav-links a.signup {
                background: transparent;
                color: var(--primary-color);
                font-weight: 600;
                border: 2px solid var(--primary-color);
            }
            
            .nav-links a.signup:hover {
                background: rgba(255, 215, 0, 0.1);
                color: var(--primary-color);
            }

            .login-section {
                padding: 140px 20px 60px;
                max-width: 400px;
                margin: 0 auto;
            }

            .login-card {
                background: var(--header-bg);
                border-radius: 15px;
                padding: 2rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            .login-header {
                text-align: center;
                margin-bottom: 2rem;
            }

            .login-title {
                font-size: 2rem;
                margin-bottom: 0.5rem;
                color: var(--primary-color);
            }

            .login-subtitle {
                color: var(--text-muted);
            }

            .form-group {
                margin-bottom: 1.5rem;
            }

            .form-group label {
                display: block;
                margin-bottom: 0.5rem;
                color: var(--text-light);
            }

            .form-group input {
                width: 100%;
                padding: 0.75rem 1rem;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                background: var(--bg-lighter);
                color: var(--text-light);
                font-size: 1rem;
            }

            .form-group input:focus {
                outline: none;
                border-color: var(--primary-color);
            }

            .login-button {
                width: 100%;
                padding: 1rem;
                background: var(--primary-color);
                color: #000000;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .login-button:hover {
                background: var(--primary-dark);
                transform: translateY(-2px);
            }

            .error-message {
                color: var(--error-color);
                text-align: center;
                margin-bottom: 1rem;
                padding: 0.5rem;
                border-radius: 8px;
                background: rgba(255, 68, 68, 0.1);
            }
        </style>
    </head>
    <body>
        <header>
            <nav>
                <a href="/" class="logo">Know Your <span>$avings</span></a>
                <div class="nav-links">
                    <a href="/">Home</a>
                    <a href="/features">Features</a>
                    <a href="/pricing">Pricing</a>
                    <a href="/login" class="login">Login</a>
                </div>
            </nav>
        </header>

        <div class="login-section">
            <div class="login-card">
                <div class="login-header">
                    <h1 class="login-title">Welcome Back</h1>
                    <p class="login-subtitle">Please login to your account</p>
                </div>
                {% if error %}
                <div class="error-message">{{ error }}</div>
                {% endif %}
                <form method="POST">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text" id="username" name="username" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    <button type="submit" class="login-button">Login</button>
                </form>
                <div class="signup-link">
                    Don't have an account? <a href="/signup">Sign Up</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        # Here you would typically add user registration logic
        # For now, we'll just redirect to login
        return redirect(url_for('login'))
            
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Sign Up - FinanceTracker</title>
        <style>
            /* Using same styling as login page */
            :root {
                --primary-color: #FFD700;
                --primary-dark: #FFC700;
                --accent-color: #FFB700;
                --header-bg: #0A1929;
                --bg-dark: #000000;
                --bg-darker: #000000;
                --bg-lighter: #111111;
                --text-light: #ffffff;
                --text-muted: #94A3B8;
                --card-bg: #0A1929;
                --success-color: #4CAF50;
                --error-color: #FF4444;
            }
            
            /* ... existing styles from login page ... */

            .signup-section {
                padding: 140px 20px 60px;
                max-width: 400px;
                margin: 0 auto;
            }

            .signup-card {
                background: var(--header-bg);
                border-radius: 15px;
                padding: 2rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            .signup-header {
                text-align: center;
                margin-bottom: 2rem;
            }

            .signup-title {
                font-size: 2rem;
                margin-bottom: 0.5rem;
                color: var(--primary-color);
            }

            .signup-subtitle {
                color: var(--text-muted);
            }

            .form-group {
                margin-bottom: 1.5rem;
            }

            .form-group label {
                display: block;
                margin-bottom: 0.5rem;
                color: var(--text-light);
            }

            .form-group input {
                width: 100%;
                padding: 0.75rem 1rem;
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                background: var(--bg-lighter);
                color: var(--text-light);
                font-size: 1rem;
            }

            .form-group input:focus {
                outline: none;
                border-color: var(--primary-color);
            }

            .signup-button {
                width: 100%;
                padding: 1rem;
                background: var(--primary-color);
                color: #000000;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .signup-button:hover {
                background: var(--primary-dark);
                transform: translateY(-2px);
            }

            .login-link {
                text-align: center;
                margin-top: 1rem;
                color: var(--text-muted);
            }

            .login-link a {
                color: var(--primary-color);
                text-decoration: none;
            }

            .login-link a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <header>
            <nav>
                <a href="/" class="logo">Know Your <span>$avings</span></a>
                <div class="nav-links">
                    <a href="/">Home</a>
                    <a href="/features">Features</a>
                    <a href="/pricing">Pricing</a>
                    <a href="/login" class="login">Login</a>
                </div>
            </nav>
        </header>

        <div class="signup-section">
            <div class="signup-card">
                <div class="signup-header">
                    <h1 class="signup-title">Create Account</h1>
                    <p class="signup-subtitle">Start your financial journey today</p>
                </div>
                {% if error %}
                <div class="error-message">{{ error }}</div>
                {% endif %}
                <form method="POST">
                    <div class="form-group">
                        <label for="fullname">Full Name</label>
                        <input type="text" id="fullname" name="fullname" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    <div class="form-group">
                        <label for="confirm_password">Confirm Password</label>
                        <input type="password" id="confirm_password" name="confirm_password" required>
                    </div>
                    <button type="submit" class="signup-button">Create Account</button>
                </form>
                <div class="login-link">
                    Already have an account? <a href="/login">Login</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', error=error)

@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Calculate total balance from all wallets
    total_balance = db.session.query(func.sum(Wallet.balance)).scalar() or 0.0
    
    # Get all budgets based on category
    income_budgets = Budget.query.filter_by(category='Income').all()
    expense_budgets = Budget.query.filter_by(category='Expenses').all()
    
    # Calculate monthly totals from budgets
    monthly_savings = sum(budget.amount for budget in income_budgets)
    monthly_expenses = sum(budget.amount for budget in expense_budgets)
    
    # Get recent transactions
    recent_transactions = Transaction.query.order_by(
        Transaction.date.desc()
    ).limit(5).all()
    
    # Calculate percentage changes (placeholder values for now)
    balance_change = 2.3
    savings_change = 5.2
    expenses_change = 3.1
    
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard - Know Your $avings</title>
        <style>
            :root {
                --primary-color: #FFD700;
                --primary-dark: #FFC700;
                --accent-color: #FFB700;
                --header-bg: #0A1929;
                --bg-dark: #000000;
                --bg-darker: #000000;
                --text-light: #ffffff;
                --text-muted: #94A3B8;
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                background-color: var(--bg-dark);
                color: var(--text-light);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                line-height: 1.6;
            }
            
            header {
                background-color: var(--header-bg);
                position: fixed;
                width: 100%;
                height: 70px;  /* Fixed height */
                top: 0;
                left: 0;
                z-index: 1000;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            nav {
                position: relative;
                width: 1200px;  /* Fixed width */
                height: 100%;
                margin: 0 auto;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .logo {
                position: absolute;
                left: 20px;
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--text-light);
                text-decoration: none;
            }
            
            .logo span {
                color: var(--primary-color);
            }
            
            .nav-links {
                position: absolute;
                right: 20px;
                display: flex;
                align-items: center;
            }
            
            .nav-links a {
                color: var(--text-light);
                text-decoration: none;
                font-weight: 500;
                font-size: 0.95rem;
                padding: 0.5rem 1rem;
                margin: 0 0.5rem;  /* Fixed margins */
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            
            .nav-links a:hover {
                color: var(--primary-color);
                background: rgba(255, 215, 0, 0.1);
            }
            
            .nav-links a.login {
                background: var(--primary-color);
                color: #000000;
                font-weight: 600;
                margin-left: 1rem;  /* Fixed margin */
            }
            
            /* Ensure content starts below fixed header */
            .content-wrapper {
                padding-top: 90px;  /* header height + 20px */
            }
            
            .dashboard-content {
                padding: 100px 20px 40px;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .welcome-header {
                margin-bottom: 2rem;
            }
            
            .welcome-title {
                font-size: 2rem;
                margin-bottom: 0.5rem;
            }
            
            .welcome-subtitle {
                color: var(--text-muted);
            }
            
            .dashboard-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }
            
            .dashboard-card {
                background: var(--header-bg);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .card-header {
                margin-bottom: 1rem;
            }
            
            .card-title {
                font-size: 1.1rem;
                color: var(--text-muted);
                margin: 0;
            }
            
            .card-amount {
                font-size: 2rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
            }
            
            .card-trend {
                color: var(--primary-color);
                font-size: 0.9rem;
            }
            
            .recent-activity {
                background: var(--header-bg);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .activity-header {
                margin-bottom: 1rem;
            }
            
            .activity-title {
                font-size: 1.1rem;
                color: var(--text-muted);
            }
            
            .activity-list {
                list-style: none;
            }
            
            .activity-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 1rem 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .activity-item:last-child {
                border-bottom: none;
            }
            
            .activity-info {
                display: flex;
                align-items: center;
                gap: 1rem;
            }
            
            .activity-icon {
                font-size: 1.2rem;
            }
            
            .activity-details {
                display: flex;
                flex-direction: column;
            }
            
            .activity-name {
                font-weight: 500;
            }
            
            .activity-date {
                font-size: 0.9rem;
                color: var(--text-muted);
            }
            
            .activity-amount {
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <header>
            <nav>
                <a href="/" class="logo">Know Your <span>$avings</span></a>
                <div class="nav-links">
                    <a href="/dashboard">Dashboard</a>
                    <a href="/wallets">Wallets</a>
                    <a href="/budgets">Budgets</a>
                    <a href="/reports">Reports</a>
                    <a href="/settings">Settings</a>
                    <a href="/logout" class="login">Logout</a>
                </div>
            </nav>
        </header>

        <div class="content-wrapper">
            <div class="dashboard-content">
                <div class="welcome-header">
                    <h1 class="welcome-title">Welcome back!</h1>
                    <p class="welcome-subtitle">Here's your financial overview</p>
                </div>

                <div class="dashboard-grid">
                    <div class="dashboard-card">
                        <div class="card-header">
                            <h2 class="card-title">Total Balance</h2>
                        </div>
                        <div class="card-amount">${{ "%.2f"|format(total_balance) }}</div>
                        <div class="card-trend">↑ {{ "%.1f"|format(balance_change) }}% from last month</div>
                    </div>

                    <div class="dashboard-card">
                        <div class="card-header">
                            <h2 class="card-title">Monthly Income</h2>
                        </div>
                        <div class="card-amount">${{ "%.2f"|format(monthly_savings) }}</div>
                        <div class="card-trend">↑ {{ "%.1f"|format(savings_change) }}% from last month</div>
                    </div>

                    <div class="dashboard-card">
                        <div class="card-header">
                            <h2 class="card-title">Monthly Expenses</h2>
                        </div>
                        <div class="card-amount">${{ "%.2f"|format(monthly_expenses) }}</div>
                        <div class="card-trend">↓ {{ "%.1f"|format(expenses_change) }}% from last month</div>
                    </div>
                </div>

                <div class="recent-activity">
                    <div class="activity-header">
                        <h2 class="activity-title">Recent Activity</h2>
                    </div>
                    <ul class="activity-list">
                        {% for transaction in recent_transactions %}
                        <li class="activity-item">
                            <div class="activity-info">
                                <div class="activity-icon">
                                    {% if transaction.amount > 0 %}💰{% else %}💳{% endif %}
                                </div>
                                <div class="activity-details">
                                    <span class="activity-name">{{ transaction.description }}</span>
                                    <span class="activity-date">{{ transaction.date.strftime('%Y-%m-%d %H:%M') }}</span>
                                </div>
                            </div>
                            <span class="activity-amount" style="color: {{ 'var(--primary-color)' if transaction.amount > 0 else '#FF4444' }}">
                                {{ '+' if transaction.amount > 0 else '' }}${{ "%.2f"|format(transaction.amount) }}
                            </span>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', 
    total_balance=total_balance,
    monthly_savings=monthly_savings,
    monthly_expenses=monthly_expenses,
    recent_transactions=recent_transactions,
    balance_change=balance_change,
    savings_change=savings_change,
    expenses_change=expenses_change
    )

@app.route('/wallet/add', methods=['POST'])
@login_required
def add_wallet():
    name = request.form.get('name')
    wallet_type = request.form.get('type')
    
    new_wallet = Wallet(
        name=name,
        wallet_type=wallet_type
    )
    
    db.session.add(new_wallet)
    db.session.commit()
    
    flash('New wallet added successfully!', 'success')
    return redirect(url_for('wallets'))

@app.route('/wallet/add_funds', methods=['POST'])
@login_required
def add_funds():
    wallet_id = request.form.get('wallet_id')
    amount = float(request.form.get('amount'))
    
    wallet = Wallet.query.get_or_404(wallet_id)
    wallet.balance += amount
    
    transaction = Transaction(
        wallet_id=wallet_id,
        amount=amount,
        description='Funds Added',
        transaction_type='deposit'
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    flash('Funds added successfully!', 'success')
    return redirect(url_for('wallets'))

@app.route('/wallet/transfer', methods=['POST'])
@login_required
def transfer_funds():
    from_id = request.form.get('from_wallet')
    to_id = request.form.get('to_wallet')
    amount = float(request.form.get('amount'))
    
    from_wallet = Wallet.query.get_or_404(from_id)
    to_wallet = Wallet.query.get_or_404(to_id)
    
    if from_wallet.balance >= amount:
        from_wallet.balance -= amount
        to_wallet.balance += amount
        
        # Record transactions
        from_transaction = Transaction(
            wallet_id=from_id,
            amount=-amount,
            description=f'Transfer to {to_wallet.name}',
            transaction_type='transfer'
        )
        
        to_transaction = Transaction(
            wallet_id=to_id,
            amount=amount,
            description=f'Transfer from {from_wallet.name}',
            transaction_type='transfer'
        )
        
        db.session.add(from_transaction)
        db.session.add(to_transaction)
        db.session.commit()
        
        flash('Transfer completed successfully!', 'success')
    else:
        flash('Insufficient funds for transfer!', 'error')
    
    return redirect(url_for('wallets'))

# Add this new route for deleting budgets
@app.route('/budget/delete/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    db.session.delete(budget)
    db.session.commit()
    flash(f'{budget.name} budget has been deleted.', 'success')
    return redirect(url_for('budgets'))

@app.route('/budget/update/<int:budget_id>', methods=['POST'])
@login_required
def update_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    if request.form.get('action') == 'delete':
        db.session.delete(budget)
        flash(f'{budget.name} budget has been deleted.', 'success')
    else:
        budget.name = request.form.get('name')
        budget.amount = float(request.form.get('amount'))
        budget.period = request.form.get('period')
        flash(f'{budget.name} budget has been updated.', 'success')
    
    db.session.commit()
    return redirect(url_for('budgets'))

# Add these routes for wallet management
@app.route('/wallet/update/<int:wallet_id>', methods=['POST'])
@login_required
def update_wallet(wallet_id):
    wallet = Wallet.query.get_or_404(wallet_id)
    
    if request.form.get('action') == 'delete':
        # First delete all transactions associated with this wallet
        Transaction.query.filter_by(wallet_id=wallet_id).delete()
        # Then delete the wallet
        db.session.delete(wallet)
        flash('Wallet and associated transactions deleted successfully!', 'success')
    else:
        wallet.name = request.form.get('name')
        wallet.wallet_type = request.form.get('type')
        flash('Wallet updated successfully!', 'success')
    
    db.session.commit()
    return redirect(url_for('wallets'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)