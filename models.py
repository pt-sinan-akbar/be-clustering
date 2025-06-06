from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class Algorithms(Base):
    __tablename__ = 'algorithms'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationships
    parameters = relationship("Parameters", back_populates="algorithm")
    metric_results = relationship("MetricResults", back_populates="algorithm")
    customer_clusters = relationship("CustomerCluster", back_populates="algorithm")
    clustering_results = relationship("ClusteringResults", back_populates="algorithm")

class Parameters(Base):
    __tablename__ = 'parameters'
    id = Column(Integer, primary_key=True, index=True)
    algorithm_id = Column(Integer, ForeignKey('algorithms.id'), nullable=False)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)

    # Relationships
    algorithm = relationship("Algorithms", back_populates="parameters")
    metric_results = relationship("MetricResults", back_populates="parameter")

class MetricResults(Base):
    __tablename__ = 'metric_results'
    id = Column(Integer, primary_key=True, index=True)
    algorithm_id = Column(Integer, ForeignKey('algorithms.id'), nullable=False)
    parameter_id = Column(Integer, ForeignKey('parameters.id'), nullable=False)
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)

    # Relationships
    algorithm = relationship("Algorithms", back_populates="metric_results")
    parameter = relationship("Parameters", back_populates="metric_results")

class Customers(Base):
    __tablename__ = 'customers'
    id = Column(String, primary_key=True, index=True)
    recency = Column(Float, nullable=False)
    frequency = Column(Float, nullable=False)
    monetary = Column(Float, nullable=False)
    state = Column(String, nullable=False)

    # Relationships
    customer_clusters = relationship("CustomerCluster", back_populates="customer")

class CustomerCluster(Base):
    __tablename__ = 'customer_cluster'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey('customers.id'), nullable=False)
    algorithm_id = Column(Integer, ForeignKey('algorithms.id'), nullable=False)
    cluster = Column(Integer, nullable=False)

    # one customer one cluster one algorithm
    __table_args__ = (UniqueConstraint('customer_id', 'algorithm_id', name='uc_customer_algorithm'),)

    # Relationships
    customer = relationship("Customers", back_populates="customer_clusters")
    algorithm = relationship("Algorithms", back_populates="customer_clusters")

class ClusteringResults(Base):
    __tablename__ = 'clustering_results'
    id = Column(Integer, primary_key=True, index=True)
    algorithm_id = Column(Integer, ForeignKey('algorithms.id'), nullable=False)
    cluster = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    midwest = Column(Integer, nullable=False)
    north = Column(Integer, nullable=False)
    northeast = Column(Integer, nullable=False)
    south = Column(Integer, nullable=False)
    southeast = Column(Integer, nullable=False)

    # one algorithm one clustering result
    __table_args__ = (UniqueConstraint('algorithm_id', 'cluster', name='uc_algorithm_cluster'),)

    # Relationships
    algorithm = relationship("Algorithms", back_populates="clustering_results")