function MemberItem({name, link}) {
    return (
        <li>
            <a className="members" href={link} target="_blank">
                <i className="member-icon fab fa-github"></i>
                <p className="member-name">{name}</p>
            </a>
        </li>
    )
}

export default MemberItem;