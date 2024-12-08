import './sectionLanding.css'

function SectionLanding({ img, alt, title, listItems, imgPosition}) {
    return (
        <div className={`section ${imgPosition === 'right' ? '' : 'reverse'}`}>
            <img 
                src={img} 
                alt={alt} 
            />
            <div className="text-container">
                <h2>
                    {title}
                </h2>
                <ul className="items-landing">
                {listItems.map((item, index) => (
                    <li key={index}>
                        <i className="fa fa-check-circle" aria-hidden="true"></i>
                        <span>
                            {item.split("\n").map((line, lineIndex) => (
                                <div key={lineIndex}>
                                    {line.split(" ").map((word, wordIndex) => {
                                        if (word.toLowerCase().includes("negative")) {
                                            return (
                                                <span key={wordIndex} style={{ color: "red" }}>
                                                    {word}{" "}
                                                </span>
                                            );
                                        }
                                        if (word.toLowerCase().includes("positive")) {
                                            return (
                                                <span key={wordIndex} style={{ color: "#00d049" }}>
                                                    {word}{" "}
                                                </span>
                                            );
                                        }
                                        return word + " ";
                                    })}
                                </div>
                            ))}
                        </span>
                    </li>
                ))}
                </ul>
            </div>
        </div>
    )
}

export default SectionLanding;