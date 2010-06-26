using System;
using System.Collections;
using System.Collections.Generic;


namespace spiral.ga
{
    public class Pool<T> : IEnumerable<T>
    {
        protected List<T> pool;

        private int position;

        public Pool()
        {
            pool = new List<T>();
            position = 0;
        }

        #region IEnumerable
        public IEnumerator<T> GetEnumerator()
        {
            return pool.GetEnumerator();
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return pool.GetEnumerator();
        }
        #endregion

        #region Operator overload
        public T this[int index]
        {
            get { return pool[index]; }
            set { pool.Insert(index, (T)value); }
        }
        #endregion

        public void AddRange(List<T> l)
        {
            pool.AddRange(l);
        }
    }
}
