from fastapi import Depends
from pydantic import BaseModel
from typing import List
from typing_extensions import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import pickle
import utils
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PKL_DIR = BASE_DIR / "pkl"

# initialize db
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def seeder(db: Session):
    try:
        def compare_customer_rows(*dataframes):
            for i in range(len(dataframes) - 1):
                df1 = dataframes[i]
                df2 = dataframes[i + 1]
                if not df1.equals(df2):
                    print(f"Dataframes {i} and {i + 1} are not equal.")
                    print("Differences:")
                    print(df1.compare(df2))
                else:
                    print(f"Dataframes {i} and {i + 1} are equal.")


        algorithms = [
            {"name": "K-MEANS"},
            {"name": "K-PROTOTYPES"},
            {"name": "DBSCAN"},
            {"name": "HIERARCHICAL"},
            {"name": "GMM"},
        ]

        # Check if algorithms already exist
        existing_algos = db.query(models.Algorithms).count()
        if existing_algos == 0:
            for algo_data in algorithms:
                algo = models.Algorithms(name=algo_data["name"])
                db.add(algo)
            db.flush()  # Flush to get the IDs without committing
            print(f"Added {len(algorithms)} algorithms")

        # Get algorithm IDs for parameter seeding
        kmeans = db.query(models.Algorithms).filter_by(name="K-MEANS").first()
        kprototypes = db.query(models.Algorithms).filter_by(name="K-PROTOTYPES").first()
        dbscan = db.query(models.Algorithms).filter_by(name="DBSCAN").first()
        hierarchical = db.query(models.Algorithms).filter_by(name="HIERARCHICAL").first()
        gmm = db.query(models.Algorithms).filter_by(name="GMM").first()

        parameters = [
            # K-MEANS parameters
            {"algorithm_id": kmeans.id, "name": "n_clusters", "value": "4"},
            {"algorithm_id": kmeans.id, "name": "random_state", "value": "42"},

            # K-PROTOTYPES parameters
            {"algorithm_id": kprototypes.id, "name": "n_clusters", "value": "5"},
            {"algorithm_id": kprototypes.id, "name": "random_state", "value": "42"},
            {"algorithm_id": kprototypes.id, "name": "init", "value": "huang"},
            {"algorithm_id": kprototypes.id, "name": "gamma", "value": "1.0"},

            # DBSCAN parameters
            {"algorithm_id": dbscan.id, "name": "eps", "value": "0.167682"},
            {"algorithm_id": dbscan.id, "name": "min_samples", "value": "13"},
            {"algorithm_id": dbscan.id, "name": "metric", "value": "euclidean"},

            # HIERARCHICAL parameters
            {"algorithm_id": hierarchical.id, "name": "n_clusters", "value": "4"},
            {"algorithm_id": hierarchical.id, "name": "linkage", "value": "ward"},

            # GMM parameters
            {"algorithm_id": gmm.id, "name": "n_components", "value": "3"},
            {"algorithm_id": gmm.id, "name": "random_state", "value": "42"},
        ]

        # Check if parameters already exist
        existing_params = db.query(models.Parameters).count()
        if existing_params == 0:
            for param_data in parameters:
                param = models.Parameters(
                    algorithm_id=param_data["algorithm_id"],
                    name=param_data["name"],
                    value=param_data["value"]
                )
                db.add(param)
            print(f"Added {len(parameters)} parameters")

        # Add customers 
        # import pkl
        dbscan_customers = utils.import_pickle(PKL_DIR / "dbscan_clean_result.pkl")
        hierarchical_customers = utils.import_pickle(PKL_DIR / "hierarchical_clean_result.pkl")
        gmm_customers = utils.import_pickle(PKL_DIR / "gmm_clean_result.pkl")
        kmeans_customers = utils.import_pickle(PKL_DIR / "kmeans_clean_result.pkl")
        kprototypes_customers = utils.import_pickle(PKL_DIR / "kprototype_clean_result.pkl")
        rfmd_clean = utils.import_pickle(PKL_DIR / "rfmd_clean.pkl")

        # # Map State column for all customer DataFrames
        # dbscan_customers = map_state_column(dbscan_customers)
        # hierarchical_customers = map_state_column(hierarchical_customers)
        # gmm_customers = map_state_column(gmm_customers)
        # kmeans_customers = map_state_column(kmeans_customers)
        # kprototypes_customers = map_state_column(kprototypes_customers)

        # print all head
        print("DBSCAN Customers head:\n", dbscan_customers.head())
        print("Hierarchical Customers head:\n", hierarchical_customers.head())
        print("GMM Customers head:\n", gmm_customers.head())
        print("KMeans Customers head:\n", kmeans_customers.head())
        print("KPrototypes Customers head:\n", kprototypes_customers.head())
        print("RFMD Clean head:\n", rfmd_clean.head())

        # copy
        rfmd_dummy = rfmd_clean.copy()
        dbscan_dummy = dbscan_customers.copy()
        hierarchical_dummy = hierarchical_customers.copy()
        gmm_dummy = gmm_customers.copy()
        kmeans_dummy = kmeans_customers.copy()
        kprototypes_dummy = kprototypes_customers.copy()

        rfmd_dummy.drop(columns=['customer_unique_id', 'State'], inplace=True)
        dbscan_dummy.drop(columns=['Cluster', 'State'], inplace=True)
        hierarchical_dummy.drop(columns=['Cluster', 'State'], inplace=True)
        gmm_dummy.drop(columns=['Cluster', 'State'], inplace=True)
        kmeans_dummy.drop(columns=['Cluster', 'State'], inplace=True)
        kprototypes_dummy.drop(columns=['Cluster', 'State'], inplace=True)

        # Perform comparison
        compare_customer_rows(
            rfmd_dummy,
            dbscan_dummy,
            hierarchical_dummy,
            gmm_dummy,
            kmeans_dummy,
            kprototypes_dummy
        )

        # add customer_unique_id to each dataframe, this value is from rfmd_clean
        dbscan_customers['customer_unique_id'] = rfmd_clean['customer_unique_id']
        hierarchical_customers['customer_unique_id'] = rfmd_clean['customer_unique_id']
        gmm_customers['customer_unique_id'] = rfmd_clean['customer_unique_id']
        kmeans_customers['customer_unique_id'] = rfmd_clean['customer_unique_id']
        kprototypes_customers['customer_unique_id'] = rfmd_clean['customer_unique_id']

        # Add customers to the Customers table
        customers_data = rfmd_clean.copy()
        customers_data["dbscan_cluster"] = dbscan_customers["Cluster"]
        customers_data["hierarchical_cluster"] = hierarchical_customers["Cluster"]
        customers_data["gmm_cluster"] = gmm_customers["Cluster"]
        customers_data["kmeans_cluster"] = kmeans_customers["Cluster"]
        customers_data["kprototypes_cluster"] = kprototypes_customers["Cluster"]

        print("Customers data shape:\n", customers_data.shape)
        print("Customers data columns:\n", customers_data.head())

        # Check if customers already exist
        existing_customers = db.query(models.Customers).count()
        if existing_customers == 0:
            for _, row in customers_data.iterrows():
                customer = models.Customers(
                    id=row["customer_unique_id"],
                    recency=row["recency"],
                    frequency=row["frequency"],
                    monetary=row["monetary"],
                    state=row["State"],
                    dbscan_cluster=row["dbscan_cluster"],
                    hierarchical_cluster=row["hierarchical_cluster"],
                    gmm_cluster=row["gmm_cluster"],
                    kmeans_cluster=row["kmeans_cluster"],
                    kprototypes_cluster=row["kprototypes_cluster"],
                )
                db.add(customer)
            print(f"Added {len(customers_data)} customers")
        else:
            print("Customers already exist in the database")

        # Eval metric results
        metric_results = [
            # K-MEANS
            {"algorithm_id": kmeans.id, "metric": "silhouette_score", "value": 0.38126101349493235},
            {"algorithm_id": kmeans.id, "metric": "davies_bouldin_score", "value": 0.8363731205147535},
            {"algorithm_id": kmeans.id, "metric": "calinski_harabasz_score", "value": 70057.94458179167},

            # K-PROTOTYPES
            {"algorithm_id": kprototypes.id, "metric": "silhouette_score", "value": 0.38109071023018204},
            {"algorithm_id": kprototypes.id, "metric": "davies_bouldin_score", "value": 0.8365480774916471},
            {"algorithm_id": kprototypes.id, "metric": "calinski_harabasz_score", "value": 70061.13514411432},

            # DBCSAN
            {"algorithm_id": dbscan.id, "metric": "silhouette_score", "value": 0.40495031844445295},
            {"algorithm_id": dbscan.id, "metric": "davies_bouldin_score", "value": 0.7149640240335599},
            {"algorithm_id": dbscan.id, "metric": "calinski_harabasz_score", "value": 28186.907612665695},

            # HIERARCHICAL
            {"algorithm_id": hierarchical.id, "metric": "silhouette_score", "value": 0.34270868239107133},
            {"algorithm_id": hierarchical.id, "metric": "davies_bouldin_score", "value": 0.8740277400622041},
            {"algorithm_id": hierarchical.id, "metric": "calinski_harabasz_score", "value": 62362.57829945101},

            # GMM
            {"algorithm_id": gmm.id, "metric": "silhouette_score", "value": 0.3773216852916443},
            {"algorithm_id": gmm.id, "metric": "davies_bouldin_score", "value": 0.9766666080343073},
            {"algorithm_id": gmm.id, "metric": "calinski_harabasz_score", "value": 62422.639099319196},
        ]

        # Check if metric results already exist
        existing_metrics = db.query(models.MetricResults).count()
        if existing_metrics == 0:
            for metric_data in metric_results:
                metric = models.MetricResults(
                    algorithm_id=metric_data["algorithm_id"],
                    metric_name=metric_data["metric"],
                    metric_value=metric_data["value"]
                )
                db.add(metric)
            print(f"Added {len(metric_results)} evaluation metrics")
        else:
            print("Evaluation metrics already exist in the database")

        # clsutering results
        clustering_results = [
            # K-MEANS
            {"algorithm_id": kmeans.id, "cluster": 0, "count": 23347, "percentage": 25.55, "midwest": 1280, "north": 533, "northeast": 2442, "south": 3554, "southeast": 15538},
            {"algorithm_id": kmeans.id, "cluster": 1, "count": 29930, "percentage": 32.75, "midwest": 1917, "north": 677, "northeast": 3406, "south": 4269, "southeast": 19661},
            {"algorithm_id": kmeans.id, "cluster": 2, "count": 12157, "percentage": 13.30, "midwest": 749, "north": 197, "northeast": 1025, "south": 1772, "southeast": 8414},
            {"algorithm_id": kmeans.id, "cluster": 3, "count": 25959, "percentage": 28.40, "midwest": 1400, "north": 296, "northeast": 1735, "south": 3517, "southeast": 19011},

            # K-PROTOTYPES
            {"algorithm_id": kprototypes.id, "cluster": 0, "count": 25994, "percentage": 28.44, "midwest": 1402, "north": 298, "northeast": 1747, "south": 3516, "southeast": 19031},
            {"algorithm_id": kprototypes.id, "cluster": 1, "count": 12157, "percentage": 13.30, "midwest": 749, "north": 197, "northeast": 1025, "south": 1772, "southeast": 8414},
            {"algorithm_id": kprototypes.id, "cluster": 2, "count": 29819, "percentage": 32.63, "midwest": 1915, "north": 675, "northeast": 3397, "south": 4264, "southeast": 19568},
            {"algorithm_id": kprototypes.id, "cluster": 3, "count": 23423, "percentage": 25.63, "midwest": 1280, "north": 533, "northeast": 2439, "south": 3560, "southeast": 15611},

            # Hierarchical
            {"algorithm_id": hierarchical.id, "cluster": 0, "count": 29332, "percentage": 32.09, "midwest": 1697, "north": 691, "northeast": 3203, "south": 4416, "southeast": 19325},
            {"algorithm_id": hierarchical.id, "cluster": 1, "count": 12177, "percentage": 13.32, "midwest": 749, "north": 197, "northeast": 1025, "south": 1774, "southeast": 8432},
            {"algorithm_id": hierarchical.id, "cluster": 2, "count": 28079, "percentage": 30.72, "midwest": 1730, "north": 575, "northeast": 2995, "south": 3993, "southeast": 18786},
            {"algorithm_id": hierarchical.id, "cluster": 3, "count": 21805, "percentage": 23.86, "midwest": 1170, "north": 240, "northeast": 1385, "south": 2929, "southeast": 16081},

            # GMM
            {"algorithm_id": gmm.id, "cluster": 0, "count": 31056, "percentage": 33.98, "midwest": 1741, "north": 691, "northeast": 3179, "south": 4677, "southeast": 20768},
            {"algorithm_id": gmm.id, "cluster": 1, "count": 48160, "percentage": 52.70, "midwest": 2856, "north": 815, "northeast": 4404, "south": 6661, "southeast": 33424},
            {"algorithm_id": gmm.id, "cluster": 2, "count": 12177, "percentage": 13.32, "midwest": 749, "north": 197, "northeast": 1025, "south": 1774, "southeast": 8432},

            # DBSCAN
            {"algorithm_id": dbscan.id, "cluster": -1, "count": 347, "percentage": 0.38, "midwest": 17, "north": 7, "northeast": 18, "south": 45, "southeast": 260},
            {"algorithm_id": dbscan.id, "cluster": 0, "count": 78933, "percentage": 86.37, "midwest": 4587, "north": 1502, "northeast": 7556, "south": 11296, "southeast": 53992},
            {"algorithm_id": dbscan.id, "cluster": 1, "count": 11925, "percentage": 13.05, "midwest": 733, "north": 191, "northeast": 1010, "south": 1739, "southeast": 8252},
            {"algorithm_id": dbscan.id, "cluster": 2, "count": 188, "percentage": 0.21, "midwest": 9, "north": 3, "northeast": 24, "south": 32, "southeast": 120},
        ]

        # Check if clustering results already exist
        existing_clustering_results = db.query(models.ClusteringResults).count()
        if existing_clustering_results == 0:
            for result_data in clustering_results:
                result = models.ClusteringResults(
                    algorithm_id=result_data["algorithm_id"],
                    cluster=result_data["cluster"],
                    count=result_data["count"],
                    percentage=result_data["percentage"],
                    midwest=result_data["midwest"],
                    north=result_data["north"],
                    northeast=result_data["northeast"],
                    south=result_data["south"],
                    southeast=result_data["southeast"]
                )
                db.add(result)
            print(f"Added {len(clustering_results)} clustering results")
        else:
            print("Clustering results already exist in the database")

        db.commit()
        print("Seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise


if __name__ == "__main__":
    with SessionLocal() as db:
        seeder(db)
