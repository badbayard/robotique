scp -r -p robot@192.168.1.96:/home/robot/parcours/`ls [^__]*.py` ../parcoursRobot96/

mv ../parcoursRobot96/parcours/* ../parcoursRobot96/

rm -r ../parcoursRobot96/parcours
scp -r -p robot@192.168.1.96:/home/robot/parcours/`ls [^__]*.py` ../parcoursRobot96/
