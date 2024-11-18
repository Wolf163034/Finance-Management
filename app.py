from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from functools import wraps
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

def create_graph():
    fig = go.Figure()
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    income = [4500, 4800, 4700, 4850, 4900, 5100]
    expenses = [3800, 3900, 3850, 3700, 3800, 3900]

    fig.add_trace(go.Scatter(
        x=months,
        y=income,
        name='Income',
        line=dict(color='#FFD700', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=months,
        y=expenses,
        name='Expenses',
        line=dict(color='#94A3B8', width=3)
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8')
    )
    
    return fig.to_html(full_html=False)

def create_spending_graph():
    fig = go.Figure()
    # Basic implementation
    return fig.to_html(full_html=False)

def create_savings_graph():
    fig = go.Figure()
    # Basic implementation
    return fig.to_html(full_html=False)

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
                    <a href="/signup" class="signup">Sign Up</a>
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
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Wallets - Know Your $avings</title>
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
                --card-bg: #0A1929;
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

            .wallets-content {
                padding: 140px 20px 60px;
                max-width: 1200px;
                margin: 0 auto;
            }

            .section-header {
                margin-bottom: 2rem;
            }

            .section-title {
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                color: var(--primary-color);
            }

            .section-subtitle {
                color: var(--text-muted);
                font-size: 1.1rem;
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
                transition: transform 0.3s ease;
            }

            .wallet-card:hover {
                transform: translateY(-5px);
            }

            .wallet-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }

            .wallet-icon {
                width: 40px;
                height: 40px;
                background: rgba(255, 215, 0, 0.1);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--primary-color);
                font-size: 1.5rem;
            }

            .wallet-type {
                font-size: 1.2rem;
                color: var(--text-light);
                font-weight: 600;
            }

            .wallet-balance {
                font-size: 2rem;
                font-weight: bold;
                margin: 1rem 0;
                color: var(--primary-color);
            }

            .wallet-details {
                display: flex;
                justify-content: space-between;
                color: var(--text-muted);
                font-size: 0.9rem;
            }

            .transactions-section {
                background: var(--header-bg);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            .transactions-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1.5rem;
            }

            .transactions-title {
                font-size: 1.2rem;
                color: var(--text-light);
            }

            .transaction-list {
                list-style: none;
            }

            .transaction-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 1rem 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }

            .transaction-item:last-child {
                border-bottom: none;
            }

            .transaction-info {
                display: flex;
                align-items: center;
                gap: 1rem;
            }

            .transaction-icon {
                width: 40px;
                height: 40px;
                background: rgba(255, 215, 0, 0.1);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--primary-color);
            }

            .transaction-details {
                display: flex;
                flex-direction: column;
            }

            .transaction-name {
                color: var(--text-light);
                font-weight: 500;
            }

            .transaction-date {
                color: var(--text-muted);
                font-size: 0.9rem;
            }

            .transaction-amount {
                color: var(--primary-color);
                font-weight: 600;
            }

            .add-wallet-button {
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                width: 3.5rem;
                height: 3.5rem;
                background: var(--primary-color);
                color: var(--bg-dark);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                cursor: pointer;
                border: none;
                box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
                transition: all 0.3s ease;
            }

            .add-wallet-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(255, 215, 0, 0.4);
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

        <div class="wallets-content">
            <div class="section-header">
                <h1 class="section-title">Your Wallets</h1>
                <p class="section-subtitle">Manage all your accounts in one place</p>
            </div>

            <div class="wallets-grid">
                <div class="wallet-card">
                    <div class="wallet-header">
                        <div class="wallet-icon">💳</div>
                        <span class="wallet-type">Main Account</span>
                    </div>
                    <div class="wallet-balance">$8,459.32</div>
                    <div class="wallet-details">
                        <span>Last transaction: Today</span>
                        <span>Active</span>
                    </div>
                </div>

                <div class="wallet-card">
                    <div class="wallet-header">
                        <div class="wallet-icon">💰</div>
                        <span class="wallet-type">Savings</span>
                    </div>
                    <div class="wallet-balance">$15,240.00</div>
                    <div class="wallet-details">
                        <span>Last transaction: 2 days ago</span>
                        <span>Active</span>
                    </div>
                </div>

                <div class="wallet-card">
                    <div class="wallet-header">
                        <div class="wallet-icon">🏦</div>
                        <span class="wallet-type">Investment</span>
                    </div>
                    <div class="wallet-balance">$42,890.15</div>
                    <div class="wallet-details">
                        <span>Last transaction: 1 week ago</span>
                        <span>Active</span>
                    </div>
                </div>
            </div>

            <div class="transactions-section">
                <div class="transactions-header">
                    <h2 class="transactions-title">Recent Transactions</h2>
                </div>
                <ul class="transaction-list">
                    <li class="transaction-item">
                        <div class="transaction-info">
                            <div class="transaction-icon">🛒</div>
                            <div class="transaction-details">
                                <span class="transaction-name">Grocery Shopping</span>
                                <span class="transaction-date">Today, 3:30 PM</span>
                            </div>
                        </div>
                        <span class="transaction-amount">-$142.50</span>
                    </li>
                    <li class="transaction-item">
                        <div class="transaction-info">
                            <div class="transaction-icon">💸</div>
                            <div class="transaction-details">
                                <span class="transaction-name">Salary Deposit</span>
                                <span class="transaction-date">Yesterday</span>
                            </div>
                        </div>
                        <span class="transaction-amount">+$3,500.00</span>
                    </li>
                    <li class="transaction-item">
                        <div class="transaction-info">
                            <div class="transaction-icon">🏠</div>
                            <div class="transaction-details">
                                <span class="transaction-name">Rent Payment</span>
                                <span class="transaction-date">3 days ago</span>
                            </div>
                        </div>
                        <span class="transaction-amount">-$1,200.00</span>
                    </li>
                </ul>
            </div>

            <button class="add-wallet-button">+</button>
        </div>
    </body>
    </html>
    ''')

@app.route('/budgets')
@login_required
def budgets():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Budgets - Know Your $avings</title>
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
                --card-bg: #0A1929;
                --success-color: #4CAF50;
                --warning-color: #FFA500;
                --danger-color: #FF4444;
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

            .budgets-content {
                padding: 140px 20px 60px;
                max-width: 1200px;
                margin: 0 auto;
            }

            .section-header {
                margin-bottom: 2rem;
            }

            .section-title {
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                color: var(--primary-color);
            }

            .section-subtitle {
                color: var(--text-muted);
                font-size: 1.1rem;
            }

            .budget-overview {
                background: var(--header-bg);
                padding: 2rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 2rem;
            }

            .overview-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1.5rem;
            }

            .overview-item {
                text-align: center;
            }

            .overview-label {
                color: var(--text-muted);
                font-size: 0.9rem;
                margin-bottom: 0.5rem;
            }

            .overview-value {
                font-size: 1.8rem;
                font-weight: bold;
                color: var(--primary-color);
            }

            .budget-categories {
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
            }

            .budget-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }

            .budget-icon {
                width: 40px;
                height: 40px;
                background: rgba(255, 215, 0, 0.1);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--primary-color);
                font-size: 1.5rem;
            }

            .budget-name {
                font-size: 1.2rem;
                color: var(--text-light);
            }

            .budget-amount {
                font-size: 1.5rem;
                font-weight: bold;
                color: var(--primary-color);
                margin: 1rem 0;
            }

            .budget-progress {
                background: rgba(255, 255, 255, 0.1);
                height: 8px;
                border-radius: 4px;
                margin-bottom: 0.5rem;
                overflow: hidden;
            }

            .progress-bar {
                height: 100%;
                border-radius: 4px;
                transition: width 0.3s ease;
            }

            .progress-safe {
                background: var(--success-color);
            }

            .progress-warning {
                background: var(--warning-color);
            }

            .progress-danger {
                background: var(--danger-color);
            }

            .budget-details {
                display: flex;
                justify-content: space-between;
                color: var(--text-muted);
                font-size: 0.9rem;
            }

            .add-budget-button {
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                width: 3.5rem;
                height: 3.5rem;
                background: var(--primary-color);
                color: var(--bg-dark);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                cursor: pointer;
                border: none;
                box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
                transition: all 0.3s ease;
            }

            .add-budget-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(255, 215, 0, 0.4);
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

        <div class="budgets-content">
            <div class="section-header">
                <h1 class="section-title">Budget Planning</h1>
                <p class="section-subtitle">Track and manage your spending limits</p>
            </div>

            <div class="budget-overview">
                <div class="overview-grid">
                    <div class="overview-item">
                        <div class="overview-label">Total Budget</div>
                        <div class="overview-value">$5,000</div>
                    </div>
                    <div class="overview-item">
                        <div class="overview-label">Spent</div>
                        <div class="overview-value">$2,840</div>
                    </div>
                    <div class="overview-item">
                        <div class="overview-label">Remaining</div>
                        <div class="overview-value">$2,160</div>
                    </div>
                    <div class="overview-item">
                        <div class="overview-label">Days Left</div>
                        <div class="overview-value">16</div>
                    </div>
                </div>
            </div>

            <div class="budget-categories">
                <div class="budget-card">
                    <div class="budget-header">
                        <div class="budget-icon">🏠</div>
                        <h3 class="budget-name">Housing</h3>
                    </div>
                    <div class="budget-amount">$1,500 / $1,500</div>
                    <div class="budget-progress">
                        <div class="progress-bar progress-danger" style="width: 100%;"></div>
                    </div>
                    <div class="budget-details">
                        <span>100% used</span>
                        <span>$0 left</span>
                    </div>
                </div>

                <div class="budget-card">
                    <div class="budget-header">
                        <div class="budget-icon">🍽️</div>
                        <h3 class="budget-name">Food & Dining</h3>
                    </div>
                    <div class="budget-amount">$450 / $600</div>
                    <div class="budget-progress">
                        <div class="progress-bar progress-warning" style="width: 75%;"></div>
                    </div>
                    <div class="budget-details">
                        <span>75% used</span>
                        <span>$150 left</span>
                    </div>
                </div>

                <div class="budget-card">
                    <div class="budget-header">
                        <div class="budget-icon">🚗</div>
                        <h3 class="budget-name">Transportation</h3>
                    </div>
                    <div class="budget-amount">$180 / $400</div>
                    <div class="budget-progress">
                        <div class="progress-bar progress-safe" style="width: 45%;"></div>
                    </div>
                    <div class="budget-details">
                        <span>45% used</span>
                        <span>$220 left</span>
                    </div>
                </div>

                <div class="budget-card">
                    <div class="budget-header">
                        <div class="budget-icon">🎮</div>
                        <h3 class="budget-name">Entertainment</h3>
                    </div>
                    <div class="budget-amount">$150 / $300</div>
                    <div class="budget-progress">
                        <div class="progress-bar progress-safe" style="width: 50%;"></div>
                    </div>
                    <div class="budget-details">
                        <span>50% used</span>
                        <span>$150 left</span>
                    </div>
                </div>
            </div>

            <button class="add-budget-button">+</button>
        </div>
    </body>
    </html>
    ''')

@app.route('/reports')
@login_required
def reports():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Reports - Know Your $avings</title>
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
                --card-bg: #0A1929;
                --success-color: #4CAF50;
                --warning-color: #FFA500;
                --danger-color: #FF4444;
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

            .reports-content {
                padding: 140px 20px 60px;
                max-width: 1200px;
                margin: 0 auto;
            }

            .section-header {
                margin-bottom: 2rem;
            }

            .section-title {
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                color: var(--primary-color);
            }

            .section-subtitle {
                color: var(--text-muted);
                font-size: 1.1rem;
            }

            .report-filters {
                background: var(--header-bg);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 2rem;
                display: flex;
                gap: 1rem;
                align-items: center;
                flex-wrap: wrap;
            }

            .filter-group {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }

            .filter-label {
                color: var(--text-muted);
                font-size: 0.9rem;
            }

            .filter-select {
                background: var(--bg-dark);
                color: var(--text-light);
                border: 1px solid rgba(255, 255, 255, 0.1);
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-size: 0.9rem;
                cursor: pointer;
            }

            .filter-select:focus {
                outline: none;
                border-color: var(--primary-color);
            }

            .report-grid {
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

            .report-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }

            .report-title {
                font-size: 1.2rem;
                color: var(--text-light);
            }

            .report-value {
                font-size: 2rem;
                font-weight: bold;
                color: var(--primary-color);
                margin: 1rem 0;
            }

            .report-trend {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.9rem;
            }

            .trend-up {
                color: var(--success-color);
            }

            .trend-down {
                color: var(--danger-color);
            }

            .chart-container {
                background: var(--header-bg);
                padding: 2rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 2rem;
                min-height: 400px;
            }

            .chart-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1.5rem;
            }

            .chart-title {
                font-size: 1.2rem;
                color: var(--text-light);
            }

            .chart-legend {
                display: flex;
                gap: 1rem;
            }

            .legend-item {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                color: var(--text-muted);
                font-size: 0.9rem;
            }

            .legend-color {
                width: 12px;
                height: 12px;
                border-radius: 3px;
            }

            .download-report {
                background: var(--primary-color);
                color: var(--bg-dark);
                padding: 0.8rem 1.5rem;
                border-radius: 8px;
                text-decoration: none;
                font-weight: 600;
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                transition: all 0.3s ease;
            }

            .download-report:hover {
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
                    <a href="/dashboard">Dashboard</a>
                    <a href="/wallets">Wallets</a>
                    <a href="/budgets">Budgets</a>
                    <a href="/reports">Reports</a>
                    <a href="/settings">Settings</a>
                    <a href="/logout" class="login">Logout</a>
                </div>
            </nav>
        </header>

        <div class="reports-content">
            <div class="section-header">
                <h1 class="section-title">Financial Reports</h1>
                <p class="section-subtitle">Analyze your financial performance</p>
            </div>

            <div class="report-filters">
                <div class="filter-group">
                    <label class="filter-label">Time Period:</label>
                    <select class="filter-select">
                        <option>Last 30 Days</option>
                        <option>Last 3 Months</option>
                        <option>Last 6 Months</option>
                        <option>Last Year</option>
                        <option>Custom Range</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Category:</label>
                    <select class="filter-select">
                        <option>All Categories</option>
                        <option>Income</option>
                        <option>Expenses</option>
                        <option>Investments</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Account:</label>
                    <select class="filter-select">
                        <option>All Accounts</option>
                        <option>Main Account</option>
                        <option>Savings</option>
                        <option>Investment</option>
                    </select>
                </div>
            </div>

            <div class="report-grid">
                <div class="report-card">
                    <div class="report-header">
                        <h3 class="report-title">Total Income</h3>
                    </div>
                    <div class="report-value">$12,450</div>
                    <div class="report-trend trend-up">
                        ↑ 8.2% from last month
                    </div>
                </div>

                <div class="report-card">
                    <div class="report-header">
                        <h3 class="report-title">Total Expenses</h3>
                    </div>
                    <div class="report-value">$7,890</div>
                    <div class="report-trend trend-down">
                        ↓ 3.5% from last month
                    </div>
                </div>

                <div class="report-card">
                    <div class="report-header">
                        <h3 class="report-title">Net Savings</h3>
                    </div>
                    <div class="report-value">$4,560</div>
                    <div class="report-trend trend-up">
                        ↑ 12.4% from last month
                    </div>
                </div>
            </div>

            <div class="chart-container">
                <div class="chart-header">
                    <h3 class="chart-title">Income vs Expenses Trend</h3>
                    <div class="chart-legend">
                        <div class="legend-item">
                            <div class="legend-color" style="background: var(--primary-color)"></div>
                            <span>Income</span>
                        </div>
                        <div class="legend-item">
                            <div class="legend-color" style="background: var(--text-muted)"></div>
                            <span>Expenses</span>
                        </div>
                    </div>
                </div>
                <!-- Chart will be rendered here -->
            </div>

            <div class="chart-container">
                <div class="chart-header">
                    <h3 class="chart-title">Expense Breakdown</h3>
                </div>
                <!-- Pie chart will be rendered here -->
            </div>

            <a href="#" class="download-report">
                📊 Download Full Report
            </a>
        </div>
    </body>
    </html>
    ''')

@app.route('/settings')
@login_required
def settings():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Settings - Know Your $avings</title>
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
                --card-bg: #0A1929;
                --success-color: #4CAF50;
                --warning-color: #FFA500;
                --danger-color: #FF4444;
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

            .settings-content {
                padding: 140px 20px 60px;
                max-width: 1200px;
                margin: 0 auto;
                display: grid;
                grid-template-columns: 250px 1fr;
                gap: 2rem;
            }

            .settings-sidebar {
                background: var(--header-bg);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                height: fit-content;
            }

            .settings-nav {
                list-style: none;
            }

            .settings-nav-item {
                margin-bottom: 0.5rem;
            }

            .settings-nav-link {
                display: flex;
                align-items: center;
                gap: 0.75rem;
                padding: 0.75rem 1rem;
                color: var(--text-light);
                text-decoration: none;
                border-radius: 8px;
                transition: all 0.3s ease;
            }

            .settings-nav-link:hover,
            .settings-nav-link.active {
                background: rgba(255, 215, 0, 0.1);
                color: var(--primary-color);
            }

            .settings-main {
                background: var(--header-bg);
                padding: 2rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            .settings-section {
                margin-bottom: 2.5rem;
            }

            .settings-section:last-child {
                margin-bottom: 0;
            }

            .settings-title {
                font-size: 1.5rem;
                color: var(--primary-color);
                margin-bottom: 1.5rem;
            }

            .form-group {
                margin-bottom: 1.5rem;
            }

            .form-group label {
                display: block;
                margin-bottom: 0.5rem;
                color: var(--text-light);
            }

            .form-group input,
            .form-group select {
                width: 100%;
                padding: 0.75rem 1rem;
                background: var(--bg-dark);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: var(--text-light);
                font-size: 1rem;
            }

            .form-group input:focus,
            .form-group select:focus {
                outline: none;
                border-color: var(--primary-color);
            }

            .toggle-group {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0.75rem 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }

            .toggle-label {
                color: var(--text-light);
            }

            .toggle-description {
                color: var(--text-muted);
                font-size: 0.9rem;
                margin-top: 0.25rem;
            }

            .toggle-switch {
                position: relative;
                width: 50px;
                height: 28px;
                background: var(--bg-dark);
                border-radius: 14px;
                padding: 3px;
                transition: all 0.3s ease;
                cursor: pointer;
            }

            .toggle-switch.active {
                background: var(--primary-color);
            }

            .toggle-switch::before {
                content: '';
                position: absolute;
                width: 22px;
                height: 22px;
                border-radius: 50%;
                background: var(--text-light);
                transition: all 0.3s ease;
            }

            .toggle-switch.active::before {
                transform: translateX(22px);
            }

            .save-button {
                background: var(--primary-color);
                color: var(--bg-dark);
                padding: 0.8rem 1.5rem;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .save-button:hover {
                background: var(--primary-dark);
                transform: translateY(-2px);
            }

            .danger-zone {
                margin-top: 3rem;
                padding-top: 2rem;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }

            .danger-title {
                color: var(--danger-color);
                font-size: 1.2rem;
                margin-bottom: 1rem;
            }

            .danger-description {
                color: var(--text-muted);
                margin-bottom: 1.5rem;
            }

            .danger-button {
                background: var(--danger-color);
                color: var(--text-light);
                padding: 0.8rem 1.5rem;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .danger-button:hover {
                opacity: 0.9;
                transform: translateY(-2px);
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

        <div class="settings-content">
            <aside class="settings-sidebar">
                <ul class="settings-nav">
                    <li class="settings-nav-item">
                        <a href="#profile" class="settings-nav-link active">
                            👤 Profile
                        </a>
                    </li>
                    <li class="settings-nav-item">
                        <a href="#security" class="settings-nav-link">
                            🔒 Security
                        </a>
                    </li>
                    <li class="settings-nav-item">
                        <a href="#notifications" class="settings-nav-link">
                            🔔 Notifications
                        </a>
                    </li>
                    <li class="settings-nav-item">
                        <a href="#preferences" class="settings-nav-link">
                            ⚙️ Preferences
                        </a>
                    </li>
                    <li class="settings-nav-item">
                        <a href="#billing" class="settings-nav-link">
                            💳 Billing
                        </a>
                    </li>
                </ul>
            </aside>

            <main class="settings-main">
                <section class="settings-section" id="profile">
                    <h2 class="settings-title">Profile Settings</h2>
                    <form>
                        <div class="form-group">
                            <label for="fullname">Full Name</label>
                            <input type="text" id="fullname" value="{{ session.username }}" required>
                        </div>
                        <div class="form-group">
                            <label for="email">Email Address</label>
                            <input type="email" id="email" value="user@example.com" required>
                        </div>
                        <div class="form-group">
                            <label for="timezone">Timezone</label>
                            <select id="timezone">
                                <option>UTC (GMT+0)</option>
                                <option>Eastern Time (GMT-5)</option>
                                <option>Pacific Time (GMT-8)</option>
                                <option>Central European Time (GMT+1)</option>
                            </select>
                        </div>
                        <button type="submit" class="save-button">Save Changes</button>
                    </form>
                </section>

                <section class="settings-section" id="notifications">
                    <h2 class="settings-title">Notification Preferences</h2>
                    <div class="toggle-group">
                        <div>
                            <div class="toggle-label">Email Notifications</div>
                            <div class="toggle-description">Receive updates about your account via email</div>
                        </div>
                        <div class="toggle-switch active"></div>
                    </div>
                    <div class="toggle-group">
                        <div>
                            <div class="toggle-label">Budget Alerts</div>
                            <div class="toggle-description">Get notified when you're close to budget limits</div>
                        </div>
                        <div class="toggle-switch active"></div>
                    </div>
                    <div class="toggle-group">
                        <div>
                            <div class="toggle-label">Security Alerts</div>
                            <div class="toggle-description">Receive notifications about account security</div>
                        </div>
                        <div class="toggle-switch active"></div>
                    </div>
                </section>

                <div class="danger-zone">
                    <h3 class="danger-title">Danger Zone</h3>
                    <p class="danger-description">Once you delete your account, there is no going back. Please be certain.</p>
                    <button class="danger-button">Delete Account</button>
                </div>
            </main>
        </div>
    </body>
    </html>
    ''')

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
                    <a href="/signup" class="signup">Sign Up</a>
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
                    <a href="/signup" class="signup">Sign Up</a>
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
                    <a href="/signup" class="signup">Sign Up</a>
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
                    <a href="/signup" class="signup">Sign Up</a>
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
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Dashboard - Know Your $avings</title>
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

            .dashboard-content {
                padding: 140px 20px 60px;
                max-width: 1200px;
                margin: 0 auto;
            }

            .welcome-header {
                margin-bottom: 2rem;
            }

            .welcome-title {
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                color: var(--primary-color);
            }

            .welcome-subtitle {
                color: var(--text-muted);
                font-size: 1.1rem;
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
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }

            .card-title {
                font-size: 1.1rem;
                color: var(--text-light);
            }

            .card-amount {
                font-size: 2rem;
                font-weight: bold;
                margin: 1rem 0;
                color: var(--primary-color);
            }

            .card-trend {
                color: var(--text-muted);
                font-size: 0.9rem;
            }

            .chart-container {
                background: var(--header-bg);
                padding: 2rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 2rem;
            }

            .recent-activity {
                background: var(--header-bg);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }

            .activity-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1.5rem;
            }

            .activity-title {
                font-size: 1.2rem;
                color: var(--text-light);
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
                width: 40px;
                height: 40px;
                background: rgba(255, 215, 0, 0.1);
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--primary-color);
            }

            .activity-details {
                display: flex;
                flex-direction: column;
            }

            .activity-name {
                color: var(--text-light);
                font-weight: 500;
            }

            .activity-date {
                color: var(--text-muted);
                font-size: 0.9rem;
            }

            .activity-amount {
                color: var(--primary-color);
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

        <div class="dashboard-content">
            <div class="welcome-header">
                <h1 class="welcome-title">Welcome back, {{ session.username }}!</h1>
                <p class="welcome-subtitle">Here's your financial overview</p>
            </div>

            <div class="dashboard-grid">
                <div class="dashboard-card">
                    <div class="card-header">
                        <h2 class="card-title">Total Balance</h2>
                    </div>
                    <div class="card-amount">$12,750.35</div>
                    <div class="card-trend">↑ 2.3% from last month</div>
                </div>

                <div class="dashboard-card">
                    <div class="card-header">
                        <h2 class="card-title">Monthly Savings</h2>
                    </div>
                    <div class="card-amount">$2,840.00</div>
                    <div class="card-trend">↑ 12% from last month</div>
                </div>

                <div class="dashboard-card">
                    <div class="card-header">
                        <h2 class="card-title">Monthly Expenses</h2>
                    </div>
                    <div class="card-amount">$1,950.00</div>
                    <div class="card-trend"> 8% from last month</div>
                </div>
            </div>

            <div class="chart-container">
                <h2 class="card-title">Income vs Expenses</h2>
                <!-- Chart will be added here -->
            </div>

            <div class="recent-activity">
                <div class="activity-header">
                    <h2 class="activity-title">Recent Activity</h2>
                </div>
                <ul class="activity-list">
                    <li class="activity-item">
                        <div class="activity-info">
                            <div class="activity-icon">💳</div>
                            <div class="activity-details">
                                <span class="activity-name">Grocery Shopping</span>
                                <span class="activity-date">Today, 2:30 PM</span>
                            </div>
                        </div>
                        <span class="activity-amount">-$85.20</span>
                    </li>
                    <li class="activity-item">
                        <div class="activity-info">
                            <div class="activity-icon">💰</div>
                            <div class="activity-details">
                                <span class="activity-name">Salary Deposit</span>
                                <span class="activity-date">Yesterday</span>
                            </div>
                        </div>
                        <span class="activity-amount">+$3,500.00</span>
                    </li>
                    <li class="activity-item">
                        <div class="activity-info">
                            <div class="activity-icon">🏠</div>
                            <div class="activity-details">
                                <span class="activity-name">Rent Payment</span>
                                <span class="activity-date">2 days ago</span>
                            </div>
                        </div>
                        <span class="activity-amount">-$1,200.00</span>
                    </li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)