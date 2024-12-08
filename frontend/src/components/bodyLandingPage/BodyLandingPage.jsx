import logo from '../../assets/logo.png'
import balances from '../../assets/balances2.png'
import payments from '../../assets/payments2.png'
import debts from '../../assets/debts2.png'
import './bodyLandingPage.css'
import Card from './Card'
import SectionLanding from './sectionLanding'
import FirstSectionLanding from './FirstSectionLanding'

const cards = [
    {
        title: "Couples", 
        icon: "fa fa-heart",
        body: "Managing finances with your partner has never been easier. This app lets couples track shared expenses, from dinners to vacations, with clear breakdowns. Whether it’s splitting bills or saving for future plans, the app ensures both partners stay on the same page and avoid misunderstandings."
    },
    {
        title: "Friends",
        icon: "fa-solid fa-users",
        body: "For friends who often share costs, this app is the perfect solution. Whether it’s for group dinners, events, or weekend getaways, everyone can see who paid and what’s owed, making group finances transparent and stress-free. It’s the ideal way to keep things fair and fun!"
    },
    {
        title: "Travels",
        icon: "fa-solid fa-plane",
        body: "Traveling with friends or family? This app simplifies managing shared expenses on the go. From hotel bookings to meals, everyone can track who paid for what and what’s owed, making group travel much smoother. Say goodbye to confusion and hello to easy, transparent travel budgeting!"
    }

]

const sections = [
    {
        img: balances,
        alt: "Balances",
        title: "Transparency in your group balances",
        listItems: [
            "Easily check how much each user owes or is owed within the group",
            "Balances are automatically updated after every payment",
            "Assign custom percentages to split payments accurately",
            "If someones owes you money, you will see your balance in negative.\nOtherwise, you will see your balance in positive"
        ],
        imgPosition: "left"
    },
    {
        img: payments,
        alt: "Payments",
        title: "Payment Overview: Stay on Top of Group Expenses",
        listItems: [
            "Easily track who made each payment and when it was made",
            "View payment categories for better expense organization",
            "See the exact amount paid by each user for every transaction"
        ],
        imgPosition: "right"
    },
    {
        img: debts,
        alt: "Debts",
        title: "View and Settle Debts: Clear Your Group’s Outstanding Balances",
        listItems: [
            "Check the current status of each debt, whether it's paid or unpaid",
            "See who owes money to whom, with clear creditor and debtor details",
            "View the exact amount owed, ensuring complete transparency of the debt",
        ],
        imgPosition: "left"
    }
]

function BodyLandingPage() {
    return (       
        <>
            <FirstSectionLanding />
            <section className="body-home section-landing-page">
                {sections.map((section, _) => (
                    <SectionLanding
                        img={section.img}
                        alt={section.alt}
                        title={section.title}
                        listItems={section.listItems}
                        imgPosition={section.imgPosition}
                    />
                ))}
            </section>
            <section className="cards-section">
                <h3 className="title-cards">
                    Ideal for
                </h3>
                <div className="cards-container">
                   {cards.map((card, _) => (
                        <Card 
                            title={card.title}
                            icon={card.icon} 
                            body={card.body} 
                        />
                    ))}
                </div>
            </section>
        </> 
    )
}

export default BodyLandingPage;