import React, { useEffect, useState, useRef } from 'react';
import { BACK_URL, TypeChart, GetToken, GetUser } from '../../utils'
import LoadingSpinner from '../loadingSpinner/LoadingSpinner' 
import { useNavigate } from 'react-router-dom';
import Table from '../table/Table';
import SearchBar from '../searchBar/SearchBar';
import './groupsTable.css';

function GroupsTable() {
    const [groups, setGroups] = useState([]);
    const [filteredGroups, setFilteredGroups] = useState([]);
    const [search, setSearch] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate()
    const hasBeenFetched = useRef(false);
    const token = GetToken();
    const user = GetUser();
    const [group_length, setGroupLength] = useState(0);

    useEffect(() => {
        const fetchGroups = async () => {
            if (hasBeenFetched.current) return;
            setLoading(true);
        
            try {
                const resGroups = await fetch(`${BACK_URL}/users/${user.email}/groups/data`, {
                    method: "GET",
                    headers: {
                        "Authorization": `Bearer ${token}`,
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*",
                    },
                    cache: "no-store",
                }); 

                if (!resGroups.ok) {
                    throw new Error('Error loading the groups');
                }

                const dataGroups = await resGroups.json();

                setGroups(dataGroups);
                setGroupLength(dataGroups.length);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }

        fetchGroups();
    }, []);

    useEffect(() => {
        setFilteredGroups(
            groups.filter(group =>
                group.group_name.toLowerCase().includes(search.toLowerCase())
            )
        );
    }, [search, groups]);

    const clickOnGroup = (group) => {
        navigate(`/groups/${group.group_id}/${group.group_name}`)
    }

    if (error) {
        return <p>Error: {error}</p>;
    } 

    const columns = [
        { name: 'Group name'},
        { name: 'Balance'}
    ];

    return (
        <section className="padding-header">
            {loading ? 
                <LoadingSpinner />
            :
            <>  
                {group_length === 0 ?
                    <SectionHelp />
                    :
                    <> 
                    <div className="search-bar-groups-super-container">
                        <SearchBar placeholder="Search group..." value={search} onSearch={setSearch} />
                    </div>
                    <Table 
                        data={filteredGroups} 
                        columns={columns} 
                        onRowClick={clickOnGroup}
                        redirect={true} 
                        type={TypeChart.GROUPS}
                    />
                    </>
                }
            </>
            }
        </section>
    );
}

function SectionHelp() {
    return (
        <div className="help-section">
            <p>
                If you are seeing this it means that you do not belong to a group yet. Let me help you!
            </p>
            <p>
                If you see at the top right of this section, you will notice that you have a button to create a new group.
                <p>
                    You just have to touch it and choice a name for your group!
                </p>
            </p>
            <p>
                Additionaly, in the navbar you can see your pending invites to groups, if you have.
            </p>
        </div>
    );
}

export default GroupsTable;