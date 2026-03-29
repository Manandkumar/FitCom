def save_hiit_session(data):
    db = SessionLocal()
    try:
        session = HIITSession(**data)
        db.add(session)
        db.commit()
    finally:
        db.close()


def load_hiit_sessions(user):
    db = SessionLocal()
    try:
        sessions = db.query(HIITSession).filter(
            HIITSession.UserId == user,
            HIITSession.IsDeleted == False
        ).all()

        result = []
        for s in sessions:
            d = s.__dict__.copy()
            d.pop("_sa_instance_state", None)
            result.append(d)

        return result
    finally:
        db.close()