import GroupsTable from './groupsTable/GroupsTable'
import CreateGroupButton from './createGroupButton/createGroupButton'

function BodyHome() {
    return (
        <section className="body-home">
            <div className="groups">
                <h3>
                    Groups
                </h3>
                <CreateGroupButton className="create-group-button"/>
            </div>
            <GroupsTable />
        </section>
    )
}

export default BodyHome;