entry_drop_all = "DELETE FROM entry WHERE store_id = %d"
entry_set_syn = "UPDATE entry SET syn=%d WHERE id=%d"
entry_del = "DELETE entry WHERE id=%d"
entry_add = "INSERT INTO entry (" \
            "store_id, created, dtstamp, modified, dtstart, due, completed, progress, priority, status, " \
            "summary, location, syn, body) VALUES (" \
            ":store_id, :created, :dtstamp, :modified, :dtstart, :due, :completed, :progress, :priority, :status, " \
            ":summary, :location, :syn, :body)"
entry_upd = "UPDATE entry SET(" \
            "store_id = :store_id, created = :created, dtstamp = :dtstamp, modified = :modified, dtstart = :dtstart," \
            "due = :due, completed = :completed, progress = :progress, priority = :priority, status = :status, " \
            "summary = :summary, location = :location, syn = :syn, body = :body WHERE is = :id"
