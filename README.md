# ff
gettingESPNadp.py makes use of other repo that goes through espn API to get draft data
creates a csv file to be included and compared to fantasypros adps in ECRvESPN

ECRvESPN takes previously created espn adps, replaces the given ESPN ADPS, recalculates the
avg adp as ECR, compares this ECR v. ESPN ADP to display value for draft day if league uses
ESPN to draft. (i.e where does ESPn rank a player, and ultimately display him as a suggested player,
vs ECR, see Nick Chubb, ECR in 2nd round, due to ESPN rankings possibly be able to grab in the third round.
