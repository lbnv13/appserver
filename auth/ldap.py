from ldap3 import Server, Connection, SAFE_SYNC
from config import servername, domain,SearchBase

#ldap
server = Server(servername)
def auth_ldap(u_name,u_passw):
    conn = Connection(server, user="{}\\{}".format(domain,u_name), password=u_passw, client_strategy=SAFE_SYNC)
    conn.bind()
    try:
        conn.bind()
        user = conn.extend.standard.who_am_i().split('\\',1)[1]
    except:
        user = None
        groups =None
        displayname = None
        UUID = None
        groups =[]
    if user:
        try:
            name=conn.search(SearchBase, 
                             '(&(objectclass=person)(!(objectclass=computer))(samaccountname={}))'.format(u_name), 
                             attributes=['cn', 'MemberOf','objectGUid'])
            UUID = name[2][0]['attributes']['objectGUid']
            displayname = name[2][0]['attributes']['cn']
            groups_from_ad = name[2][0]['attributes']['memberof']
            groups =[]
            for group in groups_from_ad:
                filter = str.split(group,',')[0].split('=')[1]
                group_ad=conn.search(SearchBase, 
                             '(&(objectclass=group)(cn={}))'.format(filter), 
                             attributes=['cn','objectGUid'])
                GUID = group_ad[2][0]['attributes']['objectGUid']
                # print(GUID)
                groups.append(GUID)
        except:
            displayname = None
            UUID = None
            groups =[] 
    return UUID, user, displayname, groups 
