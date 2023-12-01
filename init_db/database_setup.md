0. checkout to the dev/init_db branch via git commands.
1. Navigate to the REPO Folder through file explorer BUT DON'T ENTER THE FOLDER (Stay outside of the folder, just find the folder)
2. Create a new folder. Name it something fitting for a database. But the name doesn't matter. This folder should be in the same directory as the one containing your REPO folder
3. Copy the file path to this new folder
4. Open up your terminal 
5. enter the following commands one by one
6. export PGPORT=8888
7. export PGHOST=/tmp
8. initdb {PASTE THE FILE PATH YOU COPIED EARLIER AND DELETE THE BRACES}
9. pg_ctl -D {paste folder path here} -o '-k /tmp' start
10. createdb $USER
11. Now use cd and enter the REPO folder
12. cd into the init_db folder
13. Open up VSCode or whatever text editor you use. Open up the makefile stored in CSE412-BlahBlahBlah/init_db
14. Paste the file path to the init_db folder for SRC_DIRECTORY
15. in your open terminal that is in the init_db directory type:
16. make setup_postgres
17. Confirm by booting up the SQL environment using psql -d $USER and run some queries.