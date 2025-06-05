from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from database import Base

class Algorithms(Base):
    __tablename__ = 'algorithms'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class Parameters(Base):
    __tablename__ = 'parameters'
    id = Column(Integer, primary_key=True, index=True)
    algorithm_id = Column(Integer, ForeignKey('algorithms.id'), nullable=False)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)

class MetricResults(Base):
    __tablename__ = 'metric_results'
    id = Column(Integer, primary_key=True, index=True)
    algorithm_id = Column(Integer, ForeignKey('algorithms.id'), nullable=False)
    parameter_id = Column(Integer, ForeignKey('parameters.id'), nullable=False)
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)

class Customers(Base):
    __tablename__ = 'customers'
    id = Column(String, primary_key=True, index=True)
    recency = Column(Float, nullable=False)
    frequency = Column(Float, nullable=False)
    monetary = Column(Float, nullable=False)
    cluster = Column(Integer, nullable=False)
    state = Column(String, nullable=False)

class ClusteringResults(Base):
    __tablename__ = 'clustering_results'
    id = Column(Integer, primary_key=True, index=True)
    algorithm_id = Column(Integer, ForeignKey('algorithms.id'), nullable=False)
    cluster = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    midwest = Column(String, nullable=False)
    north = Column(String, nullable=False)
    northeast = Column(String, nullable=False)
    south = Column(String, nullable=False)
    southeast = Column(String, nullable=False)
    



