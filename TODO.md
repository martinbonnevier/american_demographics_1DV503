## Queries

### Aggregation:
DONE! (1) SUM all democrat votes specifik year -> Total democrat votes

### Group by:
Show number of candidates, group by year 1990 - 2014
### Multi schema queries:
DONE! 1. All states with over 30% bachelor or higher education -> Which candidate a specifik year
2. List all States by income per capita -> Which party got most votes a specifik year
3. List all States by number of foreign born -> Who got most votes

### View:
DONE! Select all states with > 80% households with an internet connection


Extra: 
Refactor: Let the user choose year and party for query (1)


Super-queryn: 
"select demographics.state, filtered_election.candidate, filtered_election.max_candidatevotes, filtered_election.party_simplified, demographics.Education_Bachelors_Degree_or_Higher from demographics
join relation on demographics.id = state_id
join (select id, candidate, party_simplified, max(election.candidatevotes) as max_candidatevotes from election where election.year='2016' group by election.State) as filtered_election on filtered_election.id = election_id 
where demographics.Education_Bachelors_Degree_or_Higher > 30
group by state_id
order by demographics.Education_Bachelors_Degree_or_Higher desc"

select demographics.state, filtered_election.candidate, filtered_election.max_candidatevotes, demographics.Miscellaneous_Foreign_Born from demographics
join relation on demographics.id = state_id
join (select id, candidate, max(election.candidatevotes) as max_candidatevotes from election where election.year='2012' group by election.State) as filtered_election on filtered_election.id = election_id 
group by state_id
order by demographics.Miscellaneous_Foreign_Born desc