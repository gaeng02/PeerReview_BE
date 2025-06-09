from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone 

from .database import Base

class User (Base) :

    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String, unique = True, index = True, nullable = False)
    wallet_address = Column(String, unique = True, nullable = False)  # 사용자 지갑 주소

    # Relations
    papers = relationship("Paper", back_populates = "owner")
    comments = relationship("Comment", back_populates = "reviewer")
    assigned_reviews = relationship("Reviewer", back_populates = "user")


class Paper (Base) :

    __tablename__ = "papers"

    id = Column(Integer, primary_key = True, index = True)
    ipfs_hash = Column(String, nullable = False)           # IPFS 해시
    owner_id = Column(Integer, ForeignKey("users.id"))    # 제출자(user.id)
    tx_hash = Column(String, nullable = True, index = True)
    created_at = Column(DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))

    # Relations
    owner = relationship("User", back_populates = "papers")
    reviewers = relationship("Reviewer", back_populates = "paper")
    comments = relationship("Comment", back_populates = "paper")


class Reviewer (Base) :

    __tablename__ = "reviewers"    # 그 논문에 할당된 3명
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key = True, index = True)
    paper_id = Column(Integer, ForeignKey("papers.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    assigned_at = Column(DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))

    # Relations
    paper = relationship("Paper", back_populates = "reviewers")
    user = relationship("User", back_populates = "assigned_reviews")


class Comment (Base) :

    __tablename__ = "comments"

    id = Column(Integer, primary_key = True, index = True)
    paper_id = Column(Integer, ForeignKey("papers.id"), nullable = False)
    reviewer_id = Column(Integer, ForeignKey("reviewers.id"), nullable = False)
    ipfs_hash = Column(String, nullable = False)           # IPFS 해시 (댓글 원문)
    tx_hash = Column(String, nullable = True, index = True)
    created_at = Column(DateTime(timezone = True), default = lambda: datetime.now(timezone.utc))

    # Relations
    paper = relationship("Paper", back_populates = "comments")
    reviewer = relationship("Reviewer", back_populates = "paper", foreign_keys = [reviewer_id])
