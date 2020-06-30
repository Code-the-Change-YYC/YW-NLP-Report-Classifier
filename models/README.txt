Dependency libraries:
    -sci-kit learn : 0.22.1 or over 
    - nltk : 3.4.5 or over

Summary of findings:
    - best performer is Linear SVM which is basic model in SVM family. 
    The model accuracy is close to 89%
    - Some parameters fine tuning should be able to break us into 90% benchmark 
    - OneVsAll model has not been implement, it maybe worth to explore text clustering techniques before 
    we train OneVsAll. Clustering may surprise us of how many labels there actually should be. I believe human 
    errors on classification is normal in raw data set, so maybe worth time to check clustering and then decide 
    how we want to structure OneVsAll to reach a reasonable acccuracy to power our auto-categorizer application.
